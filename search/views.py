from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from booths.models import *
from rest_framework.permissions import AllowAny


class BoothSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", "").strip()

        # ❗ 검색어가 없을 경우 예외 처리
        if not query:
            return Response({"message": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 🔍 부스명에서 검색
        booth_results = Booth.objects.filter(Q(name__icontains=query))

        # 🔍 메뉴에서 검색한 부스를 가져오기
        menu_results = Menu.objects.filter(
            Q(name__icontains=query)).values_list("booth_id", flat=True)
        menu_booths = Booth.objects.filter(id__in=menu_results)

        # 🎯 부스명 또는 메뉴에서 검색된 부스들을 합친 후 중복 제거
        all_booths = booth_results.union(menu_booths)

        # ❗ 검색 결과가 없을 경우
        if not all_booths.exists():
            return Response({"message": "검색 결과가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        # 부스 아이디랑 이름, 공연 여부만 반환환
        results = [
            {
                "id": booth.id,
                "name": booth.name,
                "is_show": booth.is_show,
                # "location": booth.location,
                # "scrap_count": booth.scrap_count,
            }
            for booth in all_booths
        ]

        return Response(
            {
                "total_results": all_booths.count(),
                "results": results,
            },
            status=status.HTTP_200_OK,
        )
