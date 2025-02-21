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

class NoticeDetailView(APIView):
    def get(self, request, notice_id, *args, **kwargs):
        # 공지 상세 조회 (DetailView)
        try:
            notice = Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist:
            raise NotFound(detail="Notice not found")
        
        serializer = NoticeDetailSerializer(notice)
        return Response(serializer.data, status=status.HTTP_200_OK)
