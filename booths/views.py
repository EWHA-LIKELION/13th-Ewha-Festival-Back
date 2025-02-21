from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from .models import *
from scrap.models import *
from .serializers import *
from rest_framework import status 
import logging

logger = logging.getLogger('django')

# 부스 정보 조회 Mixin
class BoothDataMixin:
    def get_booth_data(self, booth_id, request):
        booth = get_object_or_404(Booth, id=booth_id)
        serializer = BoothSerializer(booth, context={'request': request})
        return serializer.data
    
    def get_operating_hours(self, booth):
        operating_hours = OperatingHours.objects.filter(booth=booth).order_by('date')
        data = []
        for hours in operating_hours:
            data.append(f'{hours.date} {hours.day_of_week} {hours.open_time} ~ {hours.close_time}')
        return data
    
    def get_is_scrap(self, user, booth):
        if user.is_authenticated:
            return Scrap.objects.exists(user=user, booth=booth)
        return False

    def get_notices(self, booth):
        notices = Notice.objects.filter(booth=booth).order_by('created_at')
        serializer = BoothNoticeSerializer(notices, many=True)
        return serializer.data
    
    def get_menus(self, booth):
        menus = Menu.objects.filter(booth=booth)
        serializer = BoothMenuSerializer(menus, many=True)
        return serializer.data
    
    def get_guest_books(self, booth, request):
        guestbooks = GuestBook.objects.filter(booth=booth)
        serializer = BoothGuestBookSerializer(guestbooks, many=True, context={'request': request})
        return serializer.data

# 부스 상세 조회(공지)
class BoothNoticeView(BoothDataMixin, views.APIView):
    def get(self, request, booth_id):
        booth_data = self.get_booth_data(booth_id, request)
        operating_hours = self.get_operating_hours(booth_id)
        is_scrap = self.get_is_scrap(request.user, booth_id)
        notices = self.get_notices(booth_id)

        data = {
            'booth': booth_data,
            'operating_hours': operating_hours,
            'is_scrap': is_scrap,
            'notices': notices
        }

        return Response(data=data, status=HTTP_200_OK)
    
# 부스 상세 조회(메뉴)
class BoothMenuView(BoothDataMixin, views.APIView):
    def get(self, request, booth_id):
        booth_data = self.get_booth_data(booth_id, request)
        operating_hours = self.get_operating_hours(booth_id)
        is_scrap = self.get_is_scrap(request.user, booth_id)
        menus = self.get_menus(booth_id)

        data = {
            'booth': booth_data,
            'operating_hours': operating_hours,
            'is_scrap': is_scrap,
            'menus': menus
        }

        return Response(data=data, status=HTTP_200_OK)

# 부스 상세 조회(방명록)
class BoothGuestBookView(BoothDataMixin, views.APIView):
    def get(self, request, booth_id):
        booth_data = self.get_booth_data(booth_id, request)
        operating_hours = self.get_operating_hours(booth_id)
        is_scrap = self.get_is_scrap(request.user, booth_id)
        guest_books = self.get_guest_books(booth_id, request)

        data = {
            'booth': booth_data,
            'operating_hours': operating_hours,
            'is_scrap': is_scrap,
            'guest_books': guest_books
        }

        return Response(data=data, status=HTTP_200_OK)
    