from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import CursorPagination
from booths.models import Booth, OperatingHours, Menu
from booths.serializers import BoothListSerializer
from search.models import SearchHistory
from booths.serializers import BoothListSerializer


# 페이지네이션 클래스 정의 (CursorPagination)
class BoothSearchPagination(CursorPagination):
    page_size = 10  # 기본 페이지 크기
    ordering = '-created_at'  # 최신 순으로 정렬
    page_size_query_param = 'page_size'  # 요청에서 페이지 크기 조절 가능
    max_page_size = 100  # 최대 페이지 크기


class BoothSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", "").strip()

        # ❗ 검색어가 없을 경우 예외 처리
        if not query:
            return Response({"message": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        q1 = Q(name__icontains=query)
        q1 &= Q(is_committee=False)

        # 🔍 부스명에서 검색
        booth_results = Booth.objects.filter(q1)

        # 🔍 메뉴에서 검색한 부스를 가져오기
        menu_results = Menu.objects.filter(
            Q(name__icontains=query)).values_list("booth_id", flat=True)
        menu_booths = Booth.objects.filter(id__in=menu_results)

        # 🎯 부스명 또는 메뉴에서 검색된 부스들을 합친 후 중복 제거
        all_booths = (booth_results | menu_booths).distinct()

        # ❗ 검색 결과가 없을 경우
        if not all_booths.exists():
            return Response({"message": "검색 결과가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        # 페이지네이션 처리 (CursorPagination 사용)
        paginator = BoothSearchPagination()
        paginated_booths = paginator.paginate_queryset(all_booths, request)

        results = BoothListSerializer(paginated_booths, many=True, context={
                                      'request': request}).data

        serializer = BoothListSerializer(
            all_booths, many=True, context={'request': request})

        # 검색 기록 저장
        if request.user.is_authenticated:
            existing_search = SearchHistory.objects.filter(
                user=request.user, query=query
            ).first()

            if existing_search:
                existing_search.save()  # `updated_at` 자동 갱신
            else:
                SearchHistory.objects.create(user=request.user, query=query)

            # ✅ 검색 기록을 `updated_at` 기준으로 정렬하여 5개까지만 유지
            user_search_history = SearchHistory.objects.filter(
                user=request.user).order_by('-updated_at')

            if user_search_history.count() > 5:
                user_search_history.last().delete()

        # 페이지네이션 응답 반환
        return paginator.get_paginated_response(results)
        return Response(
            {
                "booth_count": all_booths.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SearchHistoryView(APIView):
    """사용자의 최근 검색 기록을 조회하는 API"""
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 조회 가능

    def get(self, request):
        user = request.user
        search_history = SearchHistory.objects.filter(
            user=user
        ).order_by('-updated_at')[:5]  # ✅ updated_at 기준으로 최신 검색어 5개 정렬

        # 검색 기록을 JSON 형태로 변환
        results = [{"query": record.query, "searched_at": record.updated_at}
                   for record in search_history]

        return Response({"search_history": results}, status=status.HTTP_200_OK)
