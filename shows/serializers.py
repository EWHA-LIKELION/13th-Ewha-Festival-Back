from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils import timezone
from .models import Show, OperatingHours
from notices.models import Notice
from guestbook.models import GuestBook

def format_timedelta(td):
    if td.days >= 1:
        return f"{td.days}일 전"
    
    elif td.seconds // 3600 >= 1:
        return f"{td.seconds // 3600}시간 전"
    
    elif td.seconds // 60 >= 1:
        return f"{td.seconds // 60}분 전"
    
    else:
        return "방금 전"


class ShowSerializer(ModelSerializer):
    formatted_location = SerializerMethodField()
    is_manager = SerializerMethodField()

    class Meta:
        model = Show
        fields = ['id', 'is_manager', 'name', 'thumbnail', 'description', 'category', 'location', 'is_opened', 'scrap_count', 'formatted_location']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_formatted_location(self, obj):
        if obj.location.endswith('관'):
            obj.location = obj.location[:-1]
        return f"{obj.location}{int(obj.show_num):02}"
    
    def get_is_manager(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj == request.user.show
    
class ShowNoticeSerializer(ModelSerializer):
    formatted_created_at = SerializerMethodField()
    location = SerializerMethodField()

    class Meta:
        model = Notice
        fields = ['title', 'content', 'formatted_created_at', 'schedules']
        read_only_fields = ['created_at', 'updated_at']

    def get_formatted_created_at(self, obj):
        time_difference = timezone.now() - obj.created_at
        return format_timedelta(time_difference)
    
    def get_location(self, obj):
        show = obj.show
        return show.location
    
class ShowGuestBookSerializer(ModelSerializer):
    nickname = SerializerMethodField()
    formatted_created_at = SerializerMethodField()
    is_author = SerializerMethodField()

    class Meta:
        model = GuestBook 
        fields = ['nickname', 'content', 'is_author', 'formatted_created_at']

    def get_nickname(self, obj):
        return obj.user.nickname
        
    def get_formatted_created_at(self, obj):
        time_difference = timezone.now() - obj.created_at
        return format_timedelta(time_difference)
        
    def get_is_author(self, obj):
        request = self.context.get('request')
        return obj.user == request.user if request else False
    
class ShowPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'name', 'category', 'location', 'description', 'contact', 'thumbnail']
        read_only_fields = ['id', 'created_at', 'updated_at']

class OperatingHoursPatchSerializer(ModelSerializer):
    class Meta:
        model = OperatingHours
        fields = ['shows', 'date', 'day_of_week', 'open_time', 'close_time']