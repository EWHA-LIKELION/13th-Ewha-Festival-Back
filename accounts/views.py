from django.shortcuts import render, redirect
from rest_framework import views
from rest_framework.status import * #status 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken  
from .models import *
from .serializers import *
import requests

# Create your views here.

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