from django.db import models
#상속받아 쓸 수 있는 유저모델 :AbstractUser
from django.contrib.auth.models import AbstractUser
from booths.models import Booth

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=10, blank=True, null=True)
    is_booth = models.BooleanField(default=False)
    #email = models.EmailField(unique=True)  # 이메일 필드를 명시적으로 추가
    booth = models.ForeignKey(Booth, on_delete=models.SET_NULL, related_name='manager', null=True)
    scrap_count = models.IntegerField(default=0)

    def __str__(self):
        return self.nickname or "Unnamed"