from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils import timezone
from .models import CommitteeBooth
from scrap.models import Scrap
from booths.models import OperatingHours

def format_timedelta(td):
    if td.days >= 1:
        return f"{td.days}일 전"

    elif td.seconds // 3600 >= 1:
        return f"{td.seconds // 3600}시간 전"

    elif td.seconds // 60 >= 1:
        return f"{td.seconds // 60}분 전"

    else:
        return "방금 전"

class CommitteeBoothListSerializer(ModelSerializer):
    formatted_location = SerializerMethodField()
    images = SerializerMethodField()
    day_of_week = SerializerMethodField()
    is_scrap = SerializerMethodField()

    class Meta:
        model = CommitteeBooth
        fields = ['id', 'name', 'is_opened', 'category', 'day_of_week',
                  'formatted_location', 'scrap_count', 'description', 'images', 'is_show', 'is_scrap']

    def get_formatted_location(self, obj):
        if obj.location.endswith('관'):
            obj.location = obj.location[:-1]
        return f"{obj.location}{int(obj.booth_num):02}"

    def get_images(self, obj):
        images = []
        images.append(obj.thumbnail)
        return images

    def get_day_of_week(self, obj):
        operating_hours = OperatingHours.objects.filter(booth=obj)
        day_of_week = []
        for day in operating_hours:
            day_of_week.append(day.day_of_week[0])
        return day_of_week
    
    def get_is_scrap(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            is_scrap = Scrap.objects.filter(booth=obj, user=request.user).exists()
        else:
            is_scrap = False
        return is_scrap

class CommitteeBoothPatchSerializer(ModelSerializer):
    class Meta:
        model = CommitteeBooth
        fields = ['id', 'thumbnail', 'name', 'description',
                  'contact', 'is_opened', 'menu_count', 'notice_count']
        read_only_fields = ['id', 'created_at', 'updated_at']