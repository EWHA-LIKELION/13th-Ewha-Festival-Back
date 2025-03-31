from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils import timezone
from .models import Booth, Menu, OperatingHours
from notices.models import Notice
from guestbooks.models import GuestBook
from scrap.models import Scrap

def format_timedelta(td):
    if td.days >= 1:
        return f"{td.days}일 전"

    elif td.seconds // 3600 >= 1:
        return f"{td.seconds // 3600}시간 전"

    elif td.seconds // 60 >= 1:
        return f"{td.seconds // 60}분 전"

    else:
        return "방금 전"
    
class BoothListSerializer(ModelSerializer):
    formatted_location = SerializerMethodField()
    images = SerializerMethodField()
    day_of_week = SerializerMethodField()
    is_scrap = SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'name', 'is_opened', 'category', 'day_of_week', 'formatted_location', 'scrap_count', 'description', 'images', 'is_scrap']

    def get_formatted_location(self, obj):
        if obj.location.endswith('관'):
            obj.location = obj.location[:-1]
        return f"{obj.location}{int(obj.booth_num):02}"
    
    def get_images(self, obj):
        menus = Menu.objects.filter(booth=obj)
        images = []
        images.append(obj.thumbnail)
        for menu in (menus[0:4] if menus.count()>4 else menus):
            images.append(menu.thumbnail)
        return images
    
    def get_day_of_week(self, obj):
        operating_hours = OperatingHours.objects.filter(booth=obj)
        day_of_week = []
        for day in operating_hours:
            day_of_week.append(day.day_of_week[0])
        return day_of_week
    
    def get_is_scrap(self, obj):
        request = self.context.get('request')
        is_scrap = Scrap.objects.filter(booth=obj, user=request.user).exists()

        return is_scrap

class BoothSerializer(ModelSerializer):
    formatted_location = SerializerMethodField()
    role = SerializerMethodField()

    class Meta:
        model = Booth
        fields = ['id', 'is_show', 'role', 'name', 'thumbnail', 'description', 'category',
                  'contact', 'is_opened', 'scrap_count', 'formatted_location']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_formatted_location(self, obj):
        if obj.location.endswith('관'):
            obj.location = obj.location[:-1]
        return f"{obj.location}{int(obj.booth_num):02}"
    
    def get_role(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return "guest"
        return "admin" if obj == request.user.booth else "user"

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
    formatted_created_at = SerializerMethodField()
    is_author = SerializerMethodField()
    
    class Meta:
        model = GuestBook
        fields = ['id', 'username', 'content', 'is_author', 'formatted_created_at']

    def get_formatted_created_at(self, obj):
        time_difference = timezone.now() - obj.created_at
        return format_timedelta(time_difference)
    
    def get_is_author(self, obj):
        request = self.context.get('request')
        return obj.user == request.user if request else False

class BoothPatchSerializer(ModelSerializer):
    class Meta:
        model = Booth
        fields = ['id', 'thumbnail', 'name', 'description', 'contact', 'is_opened', 'menu_count', 'notice_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

class OperatingHoursPatchSerializer(ModelSerializer):
    class Meta:
        model = OperatingHours
        fields = ['booth', 'date', 'day_of_week', 'open_time', 'close_time']