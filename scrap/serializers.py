from rest_framework import serializers
from .models import Scrap
from booths.serializers import BoothListSerializer  # BoothListSerializer 임포트


class BoothScrapSerializer(serializers.ModelSerializer):
    booth = BoothListSerializer()  # BoothListSerializer 사용하여 부스 정보 직렬화
    user_id = serializers.IntegerField(source='user.id')  # 스크랩한 사용자의 ID 추가

    class Meta:
        model = Scrap
        # 스크랩 ID, 부스 정보, 사용자 정보 및 생성 일시 반환
        fields = ['id', 'booth', 'user_id', 'created_at']


class BoothScrapSerializer(serializers.ModelSerializer):
    booth = BoothListSerializer()  # BoothListSerializer 사용하여 부스 정보 직렬화
    user_id = serializers.IntegerField(source='user.id')  # 스크랩한 사용자의 ID 추가

    class Meta:
        model = Scrap
        # 스크랩 ID, 부스 정보, 사용자 정보 및 생성 일시 반환
        fields = ['id', 'booth', 'user_id', 'created_at']
