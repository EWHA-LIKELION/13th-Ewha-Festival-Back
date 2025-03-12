from rest_framework import serializers

from .models import *
from accounts.models import User
from django.utils.timesince import timesince

class GuestBookSerializer(serializers.ModelSerializer):
    guestbook_id = serializers.IntegerField(source='id', read_only=True)
    #user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    booth_id = serializers.IntegerField(source='booth.id', read_only=True)

    #시간 변환 위해 새로 만든 필드(2시간 전)
    created_ago = serializers.SerializerMethodField()  
 
    class Meta:
        model = GuestBook
        fields = ['booth_id','guestbook_id','username','content','created_at', 'created_ago']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
    
    def get_created_ago(self, obj):
        # timesince 함수: 현재 시간 & 특정 날짜 사이의 차이 문자열로 변환
        # 2시간 30분 전 -> 2시간 전(큰 단위만 남기기)
        time_split= timesince(obj.created_at).split(",")[0]
        return f"{time_split} 전" #문자열로 