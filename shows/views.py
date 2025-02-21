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
class ShowDataMixin:
    def get_show_data(self, show_id, request):
        show = get_object_or_404(Show, id=show_id)
        serializer = ShowSerializer(show, context={'request': request})
        return serializer.data
    
    def get_operating_hours(self, show):
        operating_hours = OperatingHours.objects.filter(show=show).order_by('date')
        data = []
        for hours in operating_hours:
            data.append(f'{hours.date} {hours.day_of_week} {hours.open_time} ~ {hours.close_time}')
        return data
    
    def get_is_scrap(self, user, show):
        if user.is_authenticated:
            return Scrap.objects.filter(user=user, show=show).exists()  # 수정된 방식
        return False


    def get_notices(self, show):
        notices = Notice.objects.filter(show=show).order_by('created_at')
        serializer = ShowNoticeSerializer(notices, many=True)
        return serializer.data
    
    
    def get_guest_books(self, show, request):
        guestbooks = GuestBook.objects.filter(show=show)
        serializer = ShowGuestBookSerializer(guestbooks, many=True, context={'request': request})
        return serializer.data

# 부스 상세 조회(공지)
class ShowNoticeView(ShowDataMixin, views.APIView):
    def get(self, request, show_id):
        show_data = self.get_show_data(show_id, request)
        operating_hours = self.get_operating_hours(show_id)
        is_scrap = self.get_is_scrap(request.user, show_id)
        notices = self.get_notices(show_id)

        data = {
            'show': show_data,
            'operating_hours': operating_hours,
            'is_scrap': is_scrap,
            'notices': notices
        }

        return Response(data=data, status=HTTP_200_OK)
    


# 부스 상세 조회(방명록)
class ShowGuestBookView(ShowDataMixin, views.APIView):
    def get(self, request, show_id):
        show_data = self.get_show_data(show_id, request)
        operating_hours = self.get_operating_hours(show_id)
        is_scrap = self.get_is_scrap(request.user, show_id)
        guest_books = self.get_guest_books(show_id, request)

        data = {
            'show': show_data,
            'operating_hours': operating_hours,
            'is_scrap': is_scrap,
            'guest_books': guest_books
        }

        return Response(data=data, status=HTTP_200_OK)
    