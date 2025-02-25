from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import *
from guestbook.models import GuestBook
from notices.models import Notice
from scrap.models import *
from .serializers import ShowSerializer, ShowNoticeSerializer, ShowGuestBookSerializer, ShowPatchSerializer, OperatingHoursPatchSerializer
from .permissions import *
from image_def import ImageProcessing
import logging
import json


# 공연 목록 조회 API
class ShowListView(APIView):

    def get(self, request, *args, **kwargs):
        # 데이터 조회
        shows = Show.objects.all()
        print(shows)  # 여기에 직접 출력해 보세요

        total_count = shows.count()
        serializer = ShowSerializer(shows, many=True, context={'request': request})
        
        return Response({"total_count": total_count, "shows": serializer.data}, status=status.HTTP_200_OK)
    
# 공연 정보 조회 Mixin
class ShowDataMixin:
    def get_show_data(self, show_id, request):
        show = get_object_or_404(Show, id=show_id)
        serializer = ShowSerializer(show, context={'request': request})
        return serializer.data
    
    def get_operating_hours(self, booth):
        operating_hours = OperatingHours.objects.filter(booth=booth).order_by('date')
        data = []
        for hours in operating_hours:
            data.append(f'{hours.date} {hours.day_of_week} {hours.open_time} ~ {hours.close_time}')
        return data
    
    def get_notices(self, show):
        notices = Notice.objects.filter(show=show).order_by('-created_at')
        serializer = ShowNoticeSerializer(notices, many=True)
        return serializer.data
    
    def get_guest_books(self, show, request):
        guest_books = GuestBook.objects.filter(show=show).order_by('-created_at')
        serializer = ShowGuestBookSerializer(guest_books, many=True, context={'request': request})
        return serializer.data

# 공연 상세 조회(공지) API
class ShowNoticeView(ShowDataMixin, APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        show_data = self.get_show_data(show_id, request)
        operating_hours = self.get_operating_hours(show)
        notices = self.get_notices(show)

        data = {
            "show": show_data,
            "operating_hours": operating_hours,
            "notices": notices
        }

        return Response(data=data, status=status.HTTP_200_OK)

# 공연 상세 조회(방명록) API
class ShowGuestBookView(ShowDataMixin, APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        show_data = self.get_show_data(show_id, request)
        operating_hours = self.get_operating_hours(show)
        guest_books = self.get_guest_books(show, request)

        data = {
            "show": show_data,
            "operating_hours": operating_hours,
            "guest_books": guest_books
        }

        return Response(data=data, status=status.HTTP_200_OK)

# 공연 수정 관련 API
class ShowPatchView(ShowDataMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        show_data = self.get_show_data(show_id, request)
        operating_hours= self.get_operating_hours(show)
        notice_count = Notice.objects.filter(show=show).count()

        data = {
            "show": show_data,
            "operating_hours": operating_hours,
            "notice_count": notice_count,
        }

        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, show_id):
        request_data = request.data.copy()
        show = get_object_or_404(Show, id=show_id)

        if 'thumbnail_image' in request_data:
            filename = f'{show.location}{int(show.show_num):02}'
            request_data['thumbnail'] = ImageProcessing.s3_file_upload_by_file_data(request_data['thumbnail_image'], "show_thumbnail", filename)

        show_serializer = ShowPatchSerializer(show, data=request_data, partial=True)

        if show_serializer.is_valid():
            show_serializer.save()

            if 'operating_hours' in request_data:
                datas = json.loads(request_data['operating_hours'])
                existing_schedules = OperatingHours.objects.filter(show=show)
                
                for schedule in existing_schedules:
                    if schedule.date not in [data['date'] for data in datas]:
                        schedule.delete()
                
                for data in datas:
                    schedule_instance = OperatingHours.objects.filter(show=show, date=data['date']).first()
                    
                    if schedule_instance:
                        schedule_serializer = OperatingHoursPatchSerializer(schedule_instance, data=data, partial=True)
                        if schedule_serializer.is_valid():
                            schedule_serializer.save()
                    else:
                        data['show'] = show_id
                        schedule_serializer = OperatingHoursPatchSerializer(data=data)
                        if schedule_serializer.is_valid():
                            schedule_serializer.save()

            return Response({"message": "공연 정보 수정 완료"}, status=status.HTTP_200_OK)
        else:
            return Response(show_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        show.delete()
        return Response({"message": "공연이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
