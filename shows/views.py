from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.response import Response
from django.db.models import Q
from booths.models import *
from guestbooks.models import GuestBook
from scrap.models import *
from booths.serializers import *
from .permissions import *
from booths.paginations import *
from image_def import ImageProcessing
import logging
import json

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
            data.append(f'{hours.date}일 {hours.day_of_week} {hours.open_time} ~ {hours.close_time}')
        return data
    
    def get_is_scrap(self, user, booth):
        if user.is_authenticated:
            return Scrap.objects.filter(user=user, booth=booth).exists()
        return False

    def get_notices(self, booth):
        notices = Notice.objects.filter(booth=booth).order_by('created_at')
        serializer = BoothNoticeSerializer(notices, many=True)
        return serializer.data
    
    def get_guest_books(self, booth, request):
        guestbooks = GuestBook.objects.filter(booth=booth).order_by('created_at')
        serializer = BoothGuestBookSerializer(guestbooks, many=True, context={'request': request})
        return serializer.data

class BoothPatchMixin:
    def get_booth_patch_data(self, booth_id):
        booth = get_object_or_404(Booth, id=booth_id)
        serializer = BoothPatchSerializer(booth)
        return serializer.data
    
    def get_operating_hours_patch(self, booth):
        operating_hours = OperatingHours.objects.filter(booth=booth)
        serializer = OperatingHoursPatchSerializer(operating_hours, many=True)
        return serializer.data

class ShowCountView(APIView, PaginationHandlerMixin):
    def get(self, request, format=None, *args, **kwargs):
        category = request.GET.getlist('category', None)
        day_of_week = request.GET.getlist('day_of_week', None)
        if day_of_week is not None:
            day_of_week = [day + '요일' for day in day_of_week]
        location = request.GET.getlist('location', None)

        q1=Q()
        q1 &= Q(is_show=True)
        q1 &= Q(is_committee=False)
        if category:
            q1 &= Q(category__in = category)
        
        if location:
            q1 &= Q(location__in = location)

        booths = Booth.objects.filter(q1)

        if day_of_week:
            for booth in booths:
                q2 = Q()
                q2 &= Q(booth = booth)
                q2 &= Q(day_of_week__in = day_of_week)
                if not OperatingHours.objects.filter(q2).exists():
                    booths.exclude(id=booth.id)  

        response = {
            "booth_count": booths.count(),
        }
        
        return Response(data=response, status=HTTP_200_OK)

# 부스 리스트 조회 API
class ShowListView(APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination
    serializer_class = BoothListSerializer

    def get(self, request, format=None, *args, **kwargs):
        category = request.GET.getlist('category', None)
        day_of_week = request.GET.getlist('day_of_week', None)
        if day_of_week is not None:
            day_of_week = [day + '요일' for day in day_of_week]
        location = request.GET.getlist('location', None)

        q1=Q()
        q1 &= Q(is_show=True)
        q1 &= Q(is_committee=False)
        if category:
            q1 &= Q(category__in = category)
        
        if location:
            q1 &= Q(location__in = location)

        booths = Booth.objects.filter(q1)

        if day_of_week:
            # 요일에 따라 운영하는 부스만 선택
            booths = booths.filter(
                operating_hours__day_of_week__in=day_of_week
            ).distinct()
        booths = booths.order_by('name')
        page = self.paginate_queryset(booths)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            serializer = self.get_paginated_response(serializer.data)
        else:
            serializer = self.serializer_class(booths, context={'request': request}, many=True)    
        
        page_count = booths.count()//10 if booths.count() % 10 == 0 else booths.count()//10 +1
        response = {
            "booth_count": booths.count(),
            "page_count": page_count,
            "booth": serializer.data
        }
        
        return Response(data=response, status=HTTP_200_OK)

# 부스 상세 조회(공지) API
class ShowNoticeView(BoothDataMixin, APIView):
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

# 부스 상세 조회(방명록) API
class ShowGuestBookView(BoothDataMixin, APIView):
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
    
# 부스 수정 관련 API
class ShowPatchView(BoothPatchMixin, APIView):
    permission_classes=[IsManager]

    def get(self, request, booth_id):
        booth_data = self.get_booth_patch_data(booth_id)
        operating_hours = self.get_operating_hours_patch(booth_id)
        data = {
            "booth": booth_data,
            "operating_hours": operating_hours
        }

        return Response(data=data, status=HTTP_200_OK)

    def patch(self, request, booth_id):
        request_data = request.data.copy()

        booth = get_object_or_404(Booth, id=booth_id)
        if 'thumbnail_image' in request_data:
            if booth.booth_num is not None:
                filename = f'{booth.location[:-1]}{int(booth.booth_num):02}{booth.name}' if booth.location.endswith('관') else f'{booth.location}{int(booth.booth_num):02}{booth.name}'
            else:
                filename = f'{booth.location[:-1]}' if booth.location.endswith('관') else f'{booth.location}'
            request_data['thumbnail'] = ImageProcessing.s3_file_upload_by_file_data(request_data['thumbnail_image'], "booth_thumbnail", filename)
            
        booth_serialzier = BoothPatchSerializer(booth, data=request_data, partial=True)

        if booth_serialzier.is_valid():
            booth_serialzier.save()

            if request_data.get('operating_hours', None):
                datas = request_data.get('operating_hours', [])
                datas = json.loads(datas)
                operating_hours = OperatingHours.objects.filter(booth=booth)

                for oh in operating_hours:
                    if oh not in [data['date'] for data in datas]:
                        oh.delete()

                for data in datas:
                    operating_hours = OperatingHours.objects.filter(booth=booth, date=data['date']).first()

                    if operating_hours:
                        operating_hours_serializer = OperatingHoursPatchSerializer(operating_hours, data=data, partial=True)

                        if operating_hours_serializer.is_valid():
                            operating_hours_serializer.save()
                        
                    else:
                        data['booth'] = booth_id
                        operating_hours_serializer = OperatingHoursPatchSerializer(data=data)

                        if operating_hours_serializer.is_valid():
                            operating_hours_serializer.save()
                    
                    

            return Response({"message": "부스 정보 수정 완료"}, status=HTTP_200_OK)