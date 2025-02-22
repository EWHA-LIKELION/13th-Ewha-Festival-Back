import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Show, PerformanceSchedule
from .serializers import *
from django.shortcuts import get_object_or_404

class ShowPatchMixin:
    def get_show_data(self, show_id):
        show = get_object_or_404(Show, id=show_id)
        return ShowSerializer(show).data
    
    def get_performance_schedule(self, show_id):
        performance_schedule = PerformanceSchedule.objects.filter(show_id=show_id).order_by('date')
        data = []
        for hours in performance_schedule:
            data.append({
                'date': hours.date,
                'day_of_week': hours.day_of_week,
                'open_time': hours.open_time,
                'close_time' : hours.close_time
            })
        return data
    

class ShowPatchView(ShowPatchMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, show_id):
        show_data = self.get_show_data(show_id)
        performance_schedule = self.get_performance_schedule(show_id)
        notice_count = Notice.objects.filter(show_id=show_id).count()
        
        data = {
            "show" : show_data,
            "performance_schedule": performance_schedule,
            "notice_count": notice_count,
        }

        return Response(data=data, status=status.HTTP_200_OK)
    
    def patch(self, request, show_id):
        request_data = request.data.copy()
        show = get_object_or_404(Show, id=show_id)

        if 'thumbnail_image' in request_data:
            filename = f'{show.location}{int(show.show_num):02}'
            request_data['thumbnail'] = ImageProcessing.s3_file_upload_file_data(request.data['thumbnail_image'], "show_thumnail", filename)

        show_serializer = ShowSerializer(show, data=request_data, partial=True)

        if show_serializer.is_valid():
            show_serializer.save()

            # 운영 시간 업데이트 처리
            if 'performance_schedule' in request_data:
                datas = json.loads(request_data['performance_schedule'])
                performance_schedule = PerformanceSchedule.objects.filter(show=show)

                # 기존 운영 시간 삭제
                for oh in performance_schedules:
                    if oh.date not in [data['date'] for data in datas]:
                        oh.delete()

                # 새로운 운영 시간 추가 또는 수정
                for data in datas:
                    performance_schedule_instance = PerformanceSchedule.objects.filter(show=show, date=data['date']).first()

                    if performance_schedule_instance:
                        performance_schedule_serializer = PerformanceSchedulePatchSerializer(performance_schedule_instance, data=data, partial=True)
                        if performance_schedule_serializer.is_valid():
                            performance_schedule_serializer.save()
                    else:
                        data['show'] = show_id
                        performance_schedule_serializer = PerformanceSchedulePatchSerializer(data=data)
                        if performance_schedule_serializer.is_valid():
                            performance_schedule_serializer.save()

            return Response({"message": "공연 정보 수정 완료"}, status=status.HTTP_200_OK)
        else:
            return Response(show_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        show.delete()
        return Response({"message": "공연이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    
class ShowNoticeView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        notices = Notice.objects.filter(show=show).order_by('-created_at')
        serializer = ShowNoticeSerializer(notices, many=True)

        data = {
            "show_id": show.id,
            "notices": serializer.data
        }

        return Response(data=data, status=status.HTTP_200_OK)


class ShowGuestBookView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        guest_books = GuestBook.objects.filter(show=show).order_by('-created_at')
        serializer = ShowGuestBookSerializer(guest_books, many=True, context={'request': request})

        data = {
            "show_id": show.id,
            "guest_books": serializer.data
        }

        return Response(data=data, status=status.HTTP_200_OK)
