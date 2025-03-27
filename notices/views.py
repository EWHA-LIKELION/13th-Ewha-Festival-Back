from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.status import *
from .models import Notice, OperationNotice
from .serializers import NoticeListSerializer, NoticeDetailSerializer, OperationNoticeSerializer
from booths.models import Booth
from .permissions import IsManagerOrReadOnly
from django.shortcuts import get_object_or_404



class NoticeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booth_id,*args, **kwargs):
        # 공지 목록 가져오기 (ListView)
        notices = Notice.objects.filter(booth__id=booth_id)
        serializer = NoticeListSerializer(notices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, booth_id, *args, **kwargs):
        booth = get_object_or_404(Booth, id=booth_id)
        if booth != request.user.booth:
            return Response(
                {"detail": "해당 부스의 관리자만 공지를 등록할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        notice = Notice.objects.create(
            title=request.data.get('title'),
            content=request.data.get('content'),
            booth=booth # 현재 로그인한 사용자
        )
        booth.increase_notice_count()
        
        
        serializer = NoticeListSerializer(notice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class NoticeDetailView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    
    def get_object(self, notice_id):
        try:
            return Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist:
            raise NotFound(detail="Notice not found")
    
    def get(self, request, notice_id, *args, **kwargs):
        notice = self.get_object(notice_id)
        serializer = NoticeDetailSerializer(notice)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, notice_id, *args, **kwargs):
        notice = self.get_object(notice_id)

        self.check_object_permissions(request, notice)

        serializer = NoticeDetailSerializer(notice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, notice_id, *args, **kwargs):
        notice = self.get_object(notice_id)

        self.check_object_permissions(request, notice)

        notice.delete()
        notice.booth.decrease_notice_count()
        return Response({"message": "Notice deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class OperationNoticeView(APIView):
    def get(self, request, *args, **kwargs):
        # 공지 목록 가져오기 (ListView)
        operation_notices = OperationNotice.objects.all().order_by('-created_at')
        serializer = OperationNoticeSerializer(operation_notices, many=True)

