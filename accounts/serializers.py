from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
import os
import environ

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_booth']
        
        # 비밀번호는 출력되지 않게 
        extra_kwargs = {'password': {'write_only': True}}  

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            is_booth=False,
        )
        user.set_password(validated_data['password'])  # 비밀번호 설정
        user.save()

        token= RefreshToken.for_user(user)
        access= str(token.access_token)

        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호입니다.')
            else:
                #토큰 생성
                token = RefreshToken.for_user(user)
                refresh = str(token)
                access = str(token.access_token)
  
            data = {
                'id': user.id,
                'username': user.username,
                'is_booth': user.is_booth,
                'access_token': access,
                'refresh_token': refresh,
            }
            return data
        else:
            raise serializers.ValidationError('존재하지 않는 사용자입니다.')
        
class KakaoLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    nickname = serializers.CharField(max_length=64, read_only=True)

    
    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호입니다.')
            else:
                token = RefreshToken.for_user(user)
                access = str(token.access_token)

                data = {
                    'id': user.id,
                    'username': user.username ,
                    'nickname': user.nickname,
                    'is_booth': user.is_booth,
                    'access_token': access
                }
                return data
        else:
            raise serializers.ValidationError('존재하지 않는 사용자입니다.')

# 환경 변수 로드
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, 'env.prod'))
KAKAO_PASSWORD = os.environ.get('KAKAO_PASSWORD')

class KakaoSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # password 필드 추가
    nickname = serializers.CharField(required=True)  
    class Meta:
        model = User
        fields = ['id', 'username','nickname', 'is_booth', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            is_booth=False
        )
        #고정 비밀번호(비밀번호 해시 저장)
        user.set_password(KAKAO_PASSWORD)
        user.save()

        return user
