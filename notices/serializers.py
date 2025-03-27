from rest_framework import serializers
from .models import Notice, OperationNotice
from django.utils import timezone
from booths.models import Booth

class OperationNoticeSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    class Meta:
        model = OperationNotice
        fields = ['id', 'title', 'content', 'created_at', 'created_date']

    def get_created_date(self, obj):
        month = obj.created_at.month  # 02월 방지 -> 2월월
        day = obj.created_at.day

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
    operating_hours = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'operating_hours', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_operating_hours(self, obj):
        operating_hours = []

        # obj.show가 주어진 경우 Show에 연결된 모든 Booth들을 가져옵니다.
        if obj.booth and obj.booth.is_show:
            show_booths = Booth.objects.filter(is_show=True)
                # 해당 부스에 연결된 운영 시간 정보를 가져옵니다.
            for booth in show_booths:
                for operating_hour in booth.operating_hours.all():  # operating_hours가 ForeignKey 또는 ManyToMany 관계라면
                    operating_hour_data = {
                        "booth": booth.id,
                        "date": operating_hour.date,  # 운영 일자
                        "day_of_week": operating_hour.day_of_week,  # 요일
                        "open_time": operating_hour.open_time,
                        "close_time": operating_hour.close_time  # 종료 시간
                    }
                    operating_hours.append(operating_hour_data)

        # obj.booth가 주어진 경우 해당 Booth의 운영 시간을 가져옵니다.
        elif obj.booth:
            booth = obj.booth
            for operating_hour in booth.operating_hours.all():
                operating_hour_data = {
                    "booth": booth.id,
                    "date": operating_hour.date,  # 운영 일자
                    "day_of_week": operating_hour.day_of_week,  # 요일
                    "open_time": operating_hour.open_time,
                    "close_time": operating_hour.close_time
                }
                operating_hours.append(operating_hour_data)

        return operating_hours
    
    
    def create(self, validated_data):
        validated_data['booth'] = self.context['request'].user
        return super().create(validated_data)

