from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.response import Response
from .models import *
from scrap.models import *
from .serializers import *
from .permissions import *
from image_def import ImageProcessing
import logging
import json

logger = logging.getLogger('django')

class MenuView(APIView):
    permission_classes = [IsManger]

    def get(self, request, booth_id):
        menus = Menu.objects.filter(booth=booth_id)
        serializer = MenuSerializer(menus, many=True)

        return Response(data=serializer.data, status=HTTP_200_OK)
    
    def post(self, request, booth_id):
        booth = get_object_or_404(Booth, id=booth_id)

        request_data = request.data.copy()
        name = request_data["name"].replace(" ", "")
        booth_num = int(booth.booth_num)

        if booth.location.endswith("관"):
            filename = f"{booth.location[:-1]}{booth_num:02}-{name}"
        else:
            filename = f"{booth.location}{booth_num:02}-{name}"
        request_data['thumbnail'] = ImageProcessing.s3_file_upload_by_file_data(request_data['thumbnail_image'], "menu_thumbnail", filename)

        serializer = MenuSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save(booth=booth)
            booth.increase_menu_count()
            return Response({"message": "메뉴 등록 완료"}, status=HTTP_200_OK)
        
        else:
            return Response({"error": serializer.error}, status=HTTP_400_BAD_REQUEST)

class MenuPatchView(APIView):
    permission_classes = [IsManger]

    def get(self, request, booth_id, menu_id):
        menu = get_object_or_404(Menu, id=menu_id)
        serializer = MenuSerializer(menu)

        return Response(data=serializer.data, status=HTTP_200_OK)
    
    def patch(self, request, booth_id, menu_id):
        request_data = request.data.copy()

        booth = get_object_or_404(Booth, id=booth_id)
        menu = get_object_or_404(Menu, id=menu_id)

        name = ""
        if 'name' in request_data:
            name = request_data['name']
            filename = f'{booth.location[:-1]}{int(booth.booth_num):02}-{menu.name.replace(" ","")}' if booth.location.endswith('관') else f'{booth.location}{int(booth.booth_num):02}-{menu.name.replace(" ","")}'
            ImageProcessing.s3_file_delete('menu_thumbnail', filename)
        else:
            name = menu.name

        if 'thumbnail_image' in request_data:
            # name = request_data['name'] if 'name' in request_data else menu.name
            name = name.replace(" ", "")
            filename = f'{booth.location[:-1]}{int(booth.booth_num):02}-{name}' if booth.location.endswith('관') else f'{booth.location}{int(booth.booth_num):02}-{name}'
            request_data['thumbnail'] = ImageProcessing.s3_file_upload_by_file_data(request_data['thumbnail_image'], "menu_thumbnail", filename)
        
        serializer = MenuSerializer(menu, data=request_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "메뉴 수정 완료"}, status=HTTP_200_OK)
        
        else:
            return Response({"error": serializer.error}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, booth_id, menu_id):
        booth = get_object_or_404(Booth, id=booth_id)
        menu = get_object_or_404(Menu, id=menu_id)
        
        name = menu.name
        filename = f'{booth.location[:-1]}{int(booth.booth_num):02}-{menu.name.replace(" ","")}' if booth.location.endswith('관') else f'{booth.location}{int(booth.booth_num):02}-{menu.name.replace(" ","")}'
        ImageProcessing.s3_file_delete('menu_thumbnail', filename)

        menu.delete()
        booth.decrease_menu_count
        return Response({"message": "메뉴 삭제 완료"}, status=HTTP_200_OK)
    
    


