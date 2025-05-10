from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.response import Response
from booths.models import Booth, OperatingHours
from booths.serializers import OperatingHoursPatchSerializer
from booths.views import BoothDataMixin, BoothPatchMixin
from .models import CommitteeBooth
from .serializers import CommitteeBoothListSerializer, CommitteeBoothPatchSerializer
from image_def import ImageProcessing
import json


# Create your views here.
class CommitteeBoothListView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        booth1 = CommitteeBooth.objects.filter(type='기획')
        booth1_serializer = CommitteeBoothListSerializer(booth1, many=True, context={'request': request})

        booth2 = CommitteeBooth.objects.filter(type='대외협력')
        booth2_serializer = CommitteeBoothListSerializer(booth2, many=True, context={'request': request})

        booth3 = CommitteeBooth.objects.filter(type='홍보디자인')
        booth3_serializer = CommitteeBoothListSerializer(booth3, many=True, context={'request': request})
        response = {
            "기획팀": booth1_serializer.data,
            "대외협력팀": booth2_serializer.data,
            "홍보디자인팀팀": booth3_serializer.data
        }
        
        return Response(data=response, status=HTTP_200_OK)
    

class CommitteeBoothView(BoothDataMixin, APIView):
    def get(self, request, booth_id):
        booth_data = self.get_booth_data(booth_id, request)
        operating_hours = self.get_operating_hours(booth_id)
        is_scrap = self.get_is_scrap(request.user, booth_id)

        data = {
            'booth': booth_data,
            'operating_hours': operating_hours,
            'is_scrap': is_scrap
        }

        return Response(data=data, status=HTTP_200_OK)
    
class CommitteeBoothPatchView(BoothPatchMixin, APIView):
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

        booth = get_object_or_404(CommitteeBooth, id=booth_id)
        if 'thumbnail_image' in request_data:
            if booth.booth_num is not None:
                filename = f'{booth.location[:-1]}{int(booth.booth_num):02}' if booth.location.endswith('관') else f'{booth.location}{int(booth.booth_num):02}'
            else:
                filename = f'{booth.location[:-1]}' if booth.location.endswith('관') else f'{booth.location}' if booth.location.endswith('관') else f'{booth.location}{int(booth.booth_num):02}'
            request_data['thumbnail'] = ImageProcessing.s3_file_upload_by_file_data(request_data['thumbnail_image'], "booth_thumbnail", filename)
            
        booth_serialzier = CommitteeBoothPatchSerializer(booth, data=request_data, partial=True)

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