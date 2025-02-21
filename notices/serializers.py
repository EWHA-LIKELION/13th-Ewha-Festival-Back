from rest_framework import serializers
from .models import Notice
from django.utils import timezone

class NoticeListSerializer(serializers.ModelSerializer):
    # 시간 차이 구하는 필드 추가 (몇 시간 전에 작성되었는지)
    time_since_created = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'time_since_created']
    
    def get_time_since_created(self, obj):
        time_difference = timezone.now() - obj.created_at
        days = time_difference.days
        hours = time_difference.seconds // 3600
        minutes = (time_difference.seconds % 3600) // 60
        if days > 0:
            return f'{days}일 전'
        elif hours > 0:
            return f'{hours}시간 전'
        elif minutes > 0:
            return f'{minutes}분 전'
        else:
            return "방금 전"

class NoticeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'operating_hours', 'contact_info', 'status', 'created_at', 'updated_at']
