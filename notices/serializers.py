from rest_framework import serializers
from .models import OperationNotice

class OperationNoticeSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    class Meta:
        model = OperationNotice
        fields = ['id', 'title', 'content', 'created_at', 'created_date']

    def get_created_date(self, obj):
        month = obj.created_at.month  # 02월 방지 -> 2월월
        day = obj.created_at.day

        return obj.created_at.strftime(f"{month}/{day}") # 월/일 형식으로 변환
