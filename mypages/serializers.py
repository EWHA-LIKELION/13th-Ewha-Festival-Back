from rest_framework import serializers
from booths.models import Booth
from scrap.models import Scrap
from accounts.models import User

# 사용자 정보 업데이트


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_booth"]
