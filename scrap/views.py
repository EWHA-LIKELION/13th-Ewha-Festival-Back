from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from .models import Booth, Scrap


class BoothScrapView(views.APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, pk=pk)

        # 이미 스크랩한 경우 처리
        if Scrap.objects.filter(booth=booth, user=request.user).exists():
            return Response({"message": "이미 스크랩 하셨습니다."}, status=HTTP_400_BAD_REQUEST)

        # 스크랩 생성
        Scrap.objects.create(booth=booth, user=request.user)

        # 🚀 스크랩 카운트 업데이트 (중요)
        booth.update_scrap_count()

        return Response({"message": "스크랩 성공", "scrap_count": booth.scrap_count}, status=HTTP_201_CREATED)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, pk=pk)
        scrap = Scrap.objects.filter(booth=booth, user=request.user).first()

        if not scrap:
            return Response({"message": "취소할 스크랩이 없습니다."}, status=HTTP_400_BAD_REQUEST)

        # 스크랩 삭제
        scrap.delete()

        # 스크랩 카운트 업데이트
        booth.update_scrap_count()

        return Response({"message": "스크랩 삭제", "scrap_count": booth.scrap_count}, status=HTTP_200_OK)
