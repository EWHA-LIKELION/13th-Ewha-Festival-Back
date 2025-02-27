from django.urls import path
from .views import *

urlpatterns = [
    path("scrapbook/", MyPageScrapView.as_view(), name="mypage-scrapbook"),  # 스크랩북 조회
    path("code/", AdminCodeView.as_view(), name="mypage-admin-code"),  # 관리자 코드 입력
    path("boothcount/", MyBoothView.as_view(), name="my-booth"),  # 관리자의 부스 조회
]