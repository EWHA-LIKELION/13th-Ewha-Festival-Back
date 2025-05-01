from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from .models import Booth, Scrap
from .serializers import BoothScrapSerializer


# 페이지네이션 클래스 정의 (CursorPagination)
class ScrapCursorPagination(CursorPagination):
    page_size = 10  # 기본 페이지 크기
    ordering = '-created_at'  # 최신 스크랩 순으로 정렬
    page_size_query_param = 'page_size'  # 쿼리 파라미터로 페이지 크기 조절 가능
    max_page_size = 100  # 최대 페이지 크기 설정


class BoothScrapView(views.APIView):
    def post(self, request, pk):
        """사용자가 부스를 스크랩하는 API"""
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, pk=pk)

        # 이미 스크랩한 경우 처리
        if Scrap.objects.filter(booth=booth, user=request.user).exists():
            return Response({"message": "이미 스크랩 하셨습니다."}, status=HTTP_400_BAD_REQUEST)

        # ✅ 스크랩 생성
        scrap = Scrap.objects.create(booth=booth, user=request.user)

        # ✅ 스크랩 카운트 증가
        request.user.increase_scrap_count()
        booth.increase_scrap_count()

        # BoothScrapSerializer를 사용하여 스크랩 정보 직렬화
        serializer = BoothScrapSerializer(scrap)

        return Response({
            "message": "스크랩 성공",
            "scrap_count": booth.scrap_count,  # 업데이트된 개수 반환
            "scrap": serializer.data  # 직렬화된 스크랩 정보 반환
        }, status=HTTP_201_CREATED)

    def delete(self, request, pk):
        """사용자가 스크랩을 취소하는 API"""
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, pk=pk)
        scrap = Scrap.objects.filter(booth=booth, user=request.user).first()

        if not scrap:
            return Response({"message": "취소할 스크랩이 없습니다."}, status=HTTP_400_BAD_REQUEST)

        # ✅ 스크랩 삭제
        scrap.delete()

        # ✅ 스크랩 카운트 감소
        request.user.decrease_scrap_count()
        booth.decrease_scrap_count()

        return Response({
            "message": "스크랩 삭제",
            "scrap_count": booth.scrap_count,  # 업데이트된 개수 반환
        }, status=HTTP_200_OK)

    def get(self, request):
        """사용자의 스크랩 목록을 페이지네이션하여 반환하는 GET 메소드"""
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        # 로그인된 사용자에 해당하는 스크랩만 필터링
        user_scraps = Scrap.objects.filter(user=request.user)

        # 페이지네이션 적용 (CursorPagination 사용)
        paginator = ScrapCursorPagination()
        paginated_scraps = paginator.paginate_queryset(user_scraps, request)

        # 스크랩 직렬화
        serializer = BoothScrapSerializer(paginated_scraps, many=True)

        # 페이지네이션 응답 반환
        return paginator.get_paginated_response(serializer.data)
