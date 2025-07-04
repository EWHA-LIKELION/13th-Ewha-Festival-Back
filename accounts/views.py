from django.shortcuts import render, redirect
from rest_framework import views
from rest_framework.status import * #status 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken  
from .models import *
from .serializers import *
import requests
import os
import environ
import logging  
from dotenv import load_dotenv
# Create your views here.

# 환경 변수 로드 (옵션: .env 파일을 사용)
load_dotenv()
#로거 생성
logger = logging.getLogger('django')

KAKAO_CLIENT_ID = os.environ.get('KAKAO_CLIENT_ID')
KAKAO_PASSWORD = os.environ.get('KAKAO_PASSWORD')
KAKAO_CLIENT_SECRET_KEY = os.environ.get('KAKAO_CLIENT_SECRET_KEY')
KAKAO_REDIRECT_URI = os.environ.get('KAKAO_REDIRECT_URI')
KAKAO_REDIRECT_PROD_URI = os.environ.get('KAKAO_REDIRECT_PROD_URI')
KAKAO_LOGIN_URI = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URI = "https://kauth.kakao.com/oauth/token"
KAKAO_PROFILE_URI = "https://kapi.kakao.com/v2/user/me"

class SignUpView(views.APIView):
    #회원가입 성공: 201, 실패: 400
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # user를 저장
            token = RefreshToken.for_user(user)  # 저장된 user로 토큰 생성

            return Response({
                'message': '회원가입 성공',
                'data': serializer.data,
                'token': str(token.access_token),
                #'refresh_token': str(token)
            }, status=HTTP_201_CREATED)
        return Response({'message': '회원가입 실패', 
                         'error': serializer.errors}, 
                         status=HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    #로그인 성공: 200, 실패: 400
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': '로그인 성공', 
                             'data': serializer.validated_data}, 
                             status=HTTP_200_OK)
        return Response({'message': '로그인 실패', 
                         'error': serializer.errors}, 
                         status=HTTP_400_BAD_REQUEST)

    
class DuplicateUsernameView(views.APIView):
    def post(self, request):
        is_duplicate = User.objects.filter(username=request.data['username']).exists()
        
        if is_duplicate:
            return Response({'message': "[사용불가]중복된 아이디입니다.",
                             'data': {"is_duplicate": is_duplicate}}, 
                             status=HTTP_200_OK)
        else:
            return Response({'message': "사용 가능한 아이디입니다.",
                             'data': {"is_duplicate": is_duplicate}}, 
                             status=HTTP_200_OK)

#카카오 로그인 
# class KakaoLoginView(views.APIView):
#     def get(self, request):
#         logging.debug("KakaoLoginView 실행")
#         kakao_url =f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
        
#         #return redirect(kakao_url)
#         return Response({'redirect_url': kakao_url}, status=200) #프론트 코드에 맞게 수정 .. (프론트에서 URL 받아서 이동)

class KakaoProdCallbackView(views.APIView):
    def get(self, request):         
        code = request.GET.get('code') # access_token 발급 위함
        if not code:
            return Response(
                {"message": "인가 코드가 없습니다. 올바른 요청인지 확인하세요."},
                status=HTTP_400_BAD_REQUEST
            )
        
        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CLIENT_ID,
            'redirect_uri': KAKAO_REDIRECT_PROD_URI,
            #CLIENT_SECRET_KEY: 추가 보안 강화
            #서버(백엔드)에서만 사용, 프론트엔드에서 절대 노출 X
            'client_secret': KAKAO_CLIENT_SECRET_KEY, 
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(KAKAO_TOKEN_URI, data=request_data, headers=token_headers)
        if token_res.status_code != 200: #카카오 API 요청이 정상적으로 처리되었는지
            return Response({'message': 'Access token 발급 실패', 
                             'error': token_res.json()}, 
                             status=HTTP_400_BAD_REQUEST)
        
        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token: #access_token이 제대로 반환되었는지 
            return Response(
                {"message": "Access token이 응답에 포함되지 않았습니다."},
                status=HTTP_400_BAD_REQUEST
            )

        # kakao 사용자 정보 불러오기
        auth_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.post(KAKAO_PROFILE_URI, headers=auth_headers)
        if user_info_res.status_code != 200:
            return Response({'message': 'kakao 사용자 정보 불러오기 실패'}, status=HTTP_400_BAD_REQUEST)
        user_info_json = user_info_res.json()
        social_id = str(user_info_json.get('id'))

        # 닉네임 가져오기
        kakao_account = user_info_json.get("kakao_account", {})
        profile = kakao_account.get("profile", {})
        #username 설정 -> 중복값 방지 
        nickname = profile.get("nickname", "")
        
        # nickname에서 공백 제거 또는 치환 → username 생성
        cleaned_nickname = nickname.replace(" ", "_")  # 공백을 밑줄로 치환
        username = cleaned_nickname + social_id

        # 회원가입 및 로그인 처리 
        try:   
            user_in_db = User.objects.get(username=username) 
            # JWT 토큰 발급
            token = RefreshToken.for_user(user_in_db)
            access_token = str(token.access_token)
            refresh_token = str(token)

            # kakao계정으로 이미 로그인한 적 있다면 -> rest-auth 로그인
            user_data = {
                'id': user_in_db.id,
                'username': user_in_db.username,
                'nickname': user_in_db.nickname,  # 닉네임 추가
                'password':  KAKAO_PASSWORD, 
                'access_token': access_token,
                'refresh_token': refresh_token,  # refresh_token 추가
                'exist': True,
            }
            #data={'username':nickname+social_id,'password':KAKAO_PASSWORD}
            serializer = KakaoLoginSerializer(data=user_data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data['exist'] = True
                validated_data['access_token'] = access_token  
                return Response({'message': "카카오 로그인 성공!", 
                                 'data': validated_data}, 
                                 status=HTTP_200_OK)
            return Response({'message': "카카오 로그인 실패", 
                             'error': serializer.errors}, 
                             status=HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            # 자동 회원가입 처리
            request_data = {
                'username': username,
                'nickname': nickname,
                'password': KAKAO_PASSWORD  # 랜덤 패스워드 사용
            }

            # 바로 회원가입 처리
            serializer = KakaoSignupSerializer(data=request_data)
            if serializer.is_valid():
                user = serializer.save()
                token = RefreshToken.for_user(user)
                access_token = str(token.access_token)
                refresh_token = str(token)

                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'nickname': user.nickname,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'exist': True,
                }

                return Response({'message': "카카오 계정 통한 회원가입 및 로그인 완료!",
                                 'data': user_data},
                                 status=HTTP_201_CREATED)
            
            return Response({'message': '카카오 계정 통한 회원가입 오류',
                             'error': serializer.errors},
                             status=HTTP_400_BAD_REQUEST)

class KakaoDevCallbackView(views.APIView):
    def get(self, request):         
        code = request.GET.get('code') # access_token 발급 위함
        if not code:
            return Response(
                {"message": "인가 코드가 없습니다. 올바른 요청인지 확인하세요."},
                status=HTTP_400_BAD_REQUEST
            )
        
        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CLIENT_ID,
            'redirect_uri': KAKAO_REDIRECT_URI,
            #CLIENT_SECRET_KEY: 추가 보안 강화
            #서버(백엔드)에서만 사용, 프론트엔드에서 절대 노출 X
            'client_secret': KAKAO_CLIENT_SECRET_KEY, 
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(KAKAO_TOKEN_URI, data=request_data, headers=token_headers)
        if token_res.status_code != 200: #카카오 API 요청이 정상적으로 처리되었는지
            return Response({'message': 'Access token 발급 실패', 
                             'error': token_res.json()}, 
                             status=HTTP_400_BAD_REQUEST)
        
        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token: #access_token이 제대로 반환되었는지 
            return Response(
                {"message": "Access token이 응답에 포함되지 않았습니다."},
                status=HTTP_400_BAD_REQUEST
            )

        # kakao 사용자 정보 불러오기
        auth_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.post(KAKAO_PROFILE_URI, headers=auth_headers)
        if user_info_res.status_code != 200:
            return Response({'message': 'kakao 사용자 정보 불러오기 실패'}, status=HTTP_400_BAD_REQUEST)
        user_info_json = user_info_res.json()
        social_id = str(user_info_json.get('id'))

        # 닉네임 가져오기
        kakao_account = user_info_json.get("kakao_account", {})
        profile = kakao_account.get("profile", {})
        #username 설정 -> 중복값 방지 
        nickname = profile.get("nickname", "")
        
        # nickname에서 공백 제거 또는 치환 → username 생성
        cleaned_nickname = nickname.replace(" ", "_")  # 공백을 밑줄로 치환
        username = cleaned_nickname + social_id

        # 회원가입 및 로그인 처리 
        try:   
            user_in_db = User.objects.get(username=username) 
            # JWT 토큰 발급
            token = RefreshToken.for_user(user_in_db)
            access_token = str(token.access_token)
            refresh_token = str(token)

            # kakao계정으로 이미 로그인한 적 있다면 -> rest-auth 로그인
            user_data = {
                'id': user_in_db.id,
                'username': user_in_db.username,
                'nickname': user_in_db.nickname,  # 닉네임 추가
                'password':  KAKAO_PASSWORD, 
                'access_token': access_token,
                'refresh_token': refresh_token,  # refresh_token 추가
                'exist': True,
            }
            #data={'username':nickname+social_id,'password':KAKAO_PASSWORD}
            serializer = KakaoLoginSerializer(data=user_data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data['exist'] = True
                validated_data['access_token'] = access_token  
                return Response({'message': "카카오 로그인 성공!", 
                                 'data': validated_data}, 
                                 status=HTTP_200_OK)
            return Response({'message': "카카오 로그인 실패", 
                             'error': serializer.errors}, 
                             status=HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            # 자동 회원가입 처리
            request_data = {
                'username': username,
                'nickname': nickname,
                'password': KAKAO_PASSWORD  # 랜덤 패스워드 사용
            }

            # 바로 회원가입 처리
            serializer = KakaoSignupSerializer(data=request_data)
            if serializer.is_valid():
                user = serializer.save()
                token = RefreshToken.for_user(user)
                access_token = str(token.access_token)
                refresh_token = str(token)

                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'nickname': user.nickname,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'exist': True,
                }

                return Response({'message': "카카오 계정 통한 회원가입 및 로그인 완료!",
                                 'data': user_data},
                                 status=HTTP_201_CREATED)
            
            return Response({'message': '카카오 계정 통한 회원가입 오류',
                             'error': serializer.errors},
                             status=HTTP_400_BAD_REQUEST)

class CustomTokenRefreshView(views.APIView):
    def post(self, request, *args, **kwargs):
        # 리프레시 토큰을 body에서 추출
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token required'}, status=HTTP_400_BAD_REQUEST)

        try:
            # 리프레시 토큰 검증 및 새로운 액세스 토큰 발급
            refresh_token = RefreshToken(refresh_token)
            access_token = str(refresh_token.access_token)

            return Response({'access_token': access_token}, status=HTTP_200_OK)

        except Exception:
            return Response({'error': '유효하지 않은 refresh token'}, status=HTTP_401_UNAUTHORIZED)