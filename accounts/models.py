from django.db import models
# 상속받아 쓸 수 있는 유저모델 :AbstractUser
from django.contrib.auth.models import AbstractUser
from booths.models import Booth
from shows.models import Show

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=10, blank=True, null=True)
    is_booth = models.BooleanField(default=False)
    booth = models.ForeignKey(Booth, on_delete=models.SET_NULL, related_name='manager', null=True)
    is_show = models.BooleanField(default=False)
    show = models.ForeignKey(Show, on_delete=models.SET_NULL, null=True, blank=True)
    scrap_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username
