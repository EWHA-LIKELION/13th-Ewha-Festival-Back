from django.db import models
# 상속받아 쓸 수 있는 유저모델 :AbstractUser
from django.contrib.auth.models import AbstractUser
from booths.models import Booth

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=10, blank=True, null=True)
    is_booth = models.BooleanField(default=False)
    booth = models.ForeignKey(Booth, on_delete=models.SET_NULL, related_name='manager', null=True)
    scrap_count = models.IntegerField(default=0)
    raw_password = models.CharField(max_length=128, null=True, blank=True)  # ✅ 평문 비밀번호 저장 필드 추가

    def increase_scrap_count(self):
        self.scrap_count += 1
        self.save(update_fields=['scrap_count'])

    def decrease_scrap_count(self):
        if self.scrap_count > 0:
            self.scrap_count -= 1
            self.save(update_fields=['scrap_count'])

    def __str__(self):
        return self.username
    
    

