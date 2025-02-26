from django.db import models
from accounts.models import User  # 유저 모델 임포트

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="search_history")
    query = models.CharField(max_length=100)  # 검색어 저장
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # 최신 검색어 기준 정렬
