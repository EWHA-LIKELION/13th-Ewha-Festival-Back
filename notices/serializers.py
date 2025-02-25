from rest_framework import serializers
<<<<<<< HEAD
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
        read_only_fields = ['created_at', 'updated_at']


    def validate(self, data):
        if not data.get('booth') and not data.get('show'):
            raise serializers.ValidationError("부스 또는 공연 중 하나는 반드시 지정해야 합니다.")
        return data

=======
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
>>>>>>> e9d92ca0af21e2580d458001d9b72b6503462804
