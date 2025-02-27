from django.db import models
from accounts.models import User
from booths.models import Booth


class Scrap(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='scrap_user')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name="scraps")

    def __str__(self):
        user_nickname = self.user.nickname if self.user and self.user.nickname else "Unknown User"
        booth_name = self.booth.name if self.booth and self.booth.name else "Unknown Booth"
        return f'{user_nickname} - {booth_name} scrap'

