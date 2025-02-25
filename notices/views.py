from rest_framework.views import APIView
from rest_framework.response import Response
<<<<<<< HEAD
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Notice
from .serializers import NoticeListSerializer, NoticeDetailSerializer

class NoticeListView(APIView):
    def get(self, request, *args, **kwargs):
        # 공지 목록 가져오기 (ListView)
        notices = Notice.objects.all()
        serializer = NoticeListSerializer(notices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = NoticeDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NoticeDetailView(APIView):
    def get_object(self, notice_id):
        try:
            return Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist:
            raise NotFound(detail="Notice not found")
    
    def get(self, request, notice_id, *args, **kwargs):
        notice = self.get_object(notice_id)
        serializer = NoticeDetailSerializer(notice)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, notice_id, *args, **kwargs):
        notice = self.get_object(notice_id)
        serializer = NoticeDetailSerializer(notice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, notice_id, *args, **kwargs):
        notice = self.get_object(notice_id)
        notice.delete()
        return Response({"message": "Notice deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
=======
from rest_framework.status import *
from .models import OperationNotice
from .serializers import OperationNoticeSerializer
# Create your views here.

class OperationNoticeView(APIView):
    def get(self, request, *args, **kwargs):
        # 공지 목록 가져오기 (ListView)
        operation_notices = OperationNotice.objects.all().order_by('-created_at')
        serializer = OperationNoticeSerializer(operation_notices, many=True)
        return Response({"message": "운영 공지 조회 성공!",
                         "data": serializer.data},
                        status=HTTP_200_OK)
 
>>>>>>> e9d92ca0af21e2580d458001d9b72b6503462804
