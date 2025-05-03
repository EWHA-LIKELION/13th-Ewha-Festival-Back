from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import *
from booths.serializers import BoothListSerializer


class BoothScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrap
        # 스크랩 ID, 부스 정보, 사용자 정보 및 생성 일시 반환
        fields = ['id', 'booth', 'user_id', 'created_at']


class BoothScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrap
        # 스크랩 ID, 부스 정보, 사용자 정보 및 생성 일시 반환
        fields = ['id', 'booth', 'user_id', 'created_at']
