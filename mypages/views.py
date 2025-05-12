from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from booths.models import Booth
from scrap.models import Scrap
from accounts.models import User
from .serializers import BoothScrapSerializer, UserSerializer
from booths.serializers import BoothListSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from guestbooks.models import GuestBook

# 마이페이지 - 스크랩북 조회 API

# 커서 페이지네이션 클래스 정의


class BoothScrapPagination(CursorPagination):
    page_size = 10  # 페이지당 항목 수
    ordering = '-created_at'  # 스크랩의 생성시간 기준으로 정렬


class MyPageScrapView(APIView):
    pagination_class = BoothScrapPagination  # 페이지네이션 클래스 적용

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        # 현재 로그인한 유저가 스크랩한 데이터 가져오기
        scraps = Scrap.objects.filter(user=request.user)

        # 커서 페이지네이션을 이용한 데이터 분리
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(scraps, request)

        booths = []
        shows = []

        # 시리얼라이저로 부스 데이터를 변환
        for scrap in result_page:
            booth_data = BoothScrapSerializer(
                scrap, context={'request': request}).data

            # 공개된 부스인지 여부에 따른 분류
            if scrap.booth.is_show:
                shows.append(booth_data)
            else:
                booths.append(booth_data)

        # 페이지네이션된 결과 반환
        return paginator.get_paginated_response({
            "booths": booths,
            "shows": shows,
            "count": len(booths) + len(shows)
        })


# 마이페이지 - 관리자 코드 입력 API
class AdminCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return Response({"message": "관리자 코드를 입력하세요."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, code=code)
        serializer = BoothListSerializer(booth, context={'request': request})

        return Response(data=serializer.data, status=HTTP_200_OK)

    def patch(self, request):
        """마이페이지 - 관리자 코드 입력"""
        user = request.user
        code = request.data.get("code")

        if not code:
            return Response({"message": "관리자 코드를 입력하세요."}, status=HTTP_400_BAD_REQUEST)

        booth = Booth.objects.filter(code=code).first()

        if not booth:
            return Response({"message": "잘못된 관리자 코드입니다."}, status=HTTP_400_BAD_REQUEST)

        user.is_booth = True
        user.booth = booth
        user.save(update_fields=["is_booth", "booth"])

        return Response({"message": "관리자 권한이 부여되었습니다."}, status=HTTP_200_OK)


class MyBoothView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # 현재 로그인한 사용자

        if not user.is_booth:
            return Response({"message": "관리자 권한이 없습니다."}, status=400)

        # 유저의 부스 정보 가져오기 (유저 모델에 이미 부스가 외래키로 연결되어 있음)
        booth = user.booth

        if not booth:
            return Response({"message": "부스 정보가 없습니다."}, status=400)

        # 해당 부스에 대한 스크랩 수와 방명록 수
        scrap_count = Scrap.objects.filter(booth=booth).count()
        guestbook_count = GuestBook.objects.filter(booth=booth).count()

        # 결과 반환
        return Response({
            "booth_name": booth.name,
            "scrap_count": scrap_count,
            "guestbook_count": guestbook_count,
            "booth_id": booth.id,
            "is_show": booth.is_show,
        })
