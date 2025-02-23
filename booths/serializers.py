from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils import timezone
from .models import Booth, Menu, OperatingHours
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

class BoothSerializer(ModelSerializer):
    formatted_location = SerializerMethodField()
    is_manager = SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'is_show', 'is_manager', 'name', 'thumbnail', 'description', 'category',
                  'contact', 'is_opened', 'scrap_count', 'formatted_location']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_formatted_location(self, obj):
        if obj.location.endswith('관'):
            obj.location = obj.location[:-1]
        return f"{obj.location}{int(obj.booth_num):02}"
    
    def get_is_manager(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return obj == request.user.booth if request else False

class BoothNoticeSerializer(ModelSerializer):
    formatted_created_at = SerializerMethodField()

    class Meta:
        model = Notice
        fields = ['title', 'content', 'formatted_created_at']

        read_only_fields = ['created_at', 'updated_at']

    def get_formatted_created_at(self, obj):
        time_difference = timezone.now() - obj.created_at
        return format_timedelta(time_difference)
    
class BoothMenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = ['thumbnail', 'name', 'price', 'is_sale']

class BoothGuestBookSerializer(ModelSerializer):
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

class BoothPatchSerializer(ModelSerializer):
    class Meta:
        model = Booth
        fields = ['id', 'thumbnail', 'name', 'description', 'contact', 'is_opened']
        read_only_fields = ['id', 'created_at', 'updated_at']

class OperatingHoursPatchSerializer(ModelSerializer):
    class Meta:
        model = OperatingHours
        fields = ['booth', 'date', 'day_of_week', 'open_time', 'close_time']