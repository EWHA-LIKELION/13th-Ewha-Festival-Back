from django.urls import path
from .views import *

urlpatterns = [
    path("booths/", BoothSearchView.as_view(), name="booth-search"),
    path("history/", SearchHistoryView.as_view(),
         name="search-history"),  # 검색 기록 조회 API

]
