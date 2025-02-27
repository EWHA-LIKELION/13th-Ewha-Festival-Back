from rest_framework import serializers
from booths.models import Booth
from scrap.models import Scrap
from accounts.models import User

# 스크랩북 조회용
class BoothScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth
        fields = ["id", "name", "location", "is_show", "scrap_count"]

# 사용자 정보 업데이트
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_booth"]
