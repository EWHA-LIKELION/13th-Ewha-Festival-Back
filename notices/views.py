from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Notice
from .serializers import NoticeListSerializer, NoticeDetailSerializer
from booths.models import Booth
from shows.models import Show


class NoticeCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        booth_id = data.get("booth_id")
        show_id = data.get("show_id")

        booth = None
        show = None

        # 부스 ID가 주어졌다면 해당 부스 가져오기
        if booth_id:
            try:
                booth = Booth.objects.get(id=booth_id)
                data["booth"] = booth.id
            except Booth.DoesNotExist:
                return Response({"error": "해당 부스가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 공연 ID가 주어졌다면 해당 공연 가져오기
        if show_id:
            try:
                show = Show.objects.get(id=show_id)
                data["show"] = show.id
            except Show.DoesNotExist:
                return Response({"error": "해당 공연이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 부스나 공연이 하나도 지정되지 않으면 오류 반환
        if not booth and not show:
            return Response({"error": "부스 또는 공연 중 하나를 지정해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NoticeDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoticeListView(APIView):
    def get(self, request, *args, **kwargs):
        # 공지 목록 가져오기 (ListView)
        notices = Notice.objects.all()
        serializer = NoticeListSerializer(notices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

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
    
    def patch(self, request, notice_id, *args, **kwargs):
        notice = self.get_object(notice_id)
        serializer = NoticeDetailSerializer(notice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, notice_id, *args, **kwargs):
        notice = self.get_object(notice_id)
        
        if notice.author != request.user:
            raise PermissionDenied(detail="삭제 권한이 없습니다.")

        notice.delete()
        return Response({"message": "Notice deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
