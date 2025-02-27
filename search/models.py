from django.db import models
from accounts.models import User  # 유저 모델 임포트
from django.conf import settings


class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="search_histories")
    query = models.CharField(max_length=255)  # 검색어
    created_at = models.DateTimeField(auto_now_add=True)  # 검색한 시간
    # 중복 검색 기록 방지를 위해 최신 검색 시간 필드 추가가
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.query}"
