from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from booths.models import Booth, Menu, OperatingHours
from search.models import SearchHistory
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination


class BoothSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", "").strip()
        page = int(request.GET.get("page", 1))  # 기본값 1페이지

        # ❗ 검색어가 없을 경우 예외 처리
        if not query:
            return Response({"message": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ 로그인한 유저의 검색 기록 저장 (최대 5개 유지)
        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=query)
            # 최근 5개만 유지 (오래된 검색어 삭제)
            search_history = SearchHistory.objects.filter(
                user=request.user).order_by('-created_at')
            if search_history.count() > 5:
                search_history.last().delete()

        # 🔍 부스명에서 검색
        booth_results = Booth.objects.filter(Q(name__icontains=query))

        # 🔍 메뉴에서 검색한 부스를 가져오기
        menu_results = Menu.objects.filter(
            Q(name__icontains=query)).values_list("booth_id", flat=True)
        menu_booths = Booth.objects.filter(id__in=menu_results)

        # 🎯 부스명 또는 메뉴에서 검색된 부스들을 합친 후 중복 제거
        all_booths = booth_results.union(menu_booths)  # `.distinct()` 제거
        all_booths = all_booths.order_by("id")  # 정렬 추가 (필수!)

        # ❗ 검색 결과가 없을 경우
        if not all_booths.exists():
            return Response({"message": "검색 결과가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        # ✅ 페이지네이션 적용 (5개씩)
        paginator = PageNumberPagination()
        paginator.page_size = 5  # 5개씩 반환
        paginated_booths = paginator.paginate_queryset(all_booths, request)

        # ✅ 부스의 운영 요일 가져오기 (OperatingHours)
        results = []
        for booth in paginated_booths:
            operating_hours = OperatingHours.objects.filter(
                booth=booth).values_list("day_of_week", flat=True)
            operation_days = list(set(operating_hours))  # 중복 제거

            results.append({
                "id": booth.id,
                "name": booth.name,
                "is_show": booth.is_show,
                "thumbnail": booth.thumbnail,
                "category": booth.category,
                "is_opened": booth.is_opened,
                "scrap_count": booth.scrap_count,
                "location": booth.location,
                "operation_days": operation_days,  # ✅ 영업 요일 리스트 포함
            })

        return Response({
            "total_results": all_booths.count(),  # 전체 검색 결과 수
            "page": page,  # 현재 페이지
            "results": results,  # 페이징된 부스 리스트
        }, status=status.HTTP_200_OK)
