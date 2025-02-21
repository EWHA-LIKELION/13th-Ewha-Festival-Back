from rest_framework.views import APIView
from rest_framework.response import Response
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
