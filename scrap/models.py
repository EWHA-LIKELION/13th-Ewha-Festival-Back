from django.db import models
from accounts.models import User
from booths.models import Booth

class Booth_scrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scrap_user')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='scrap_booth')

    def __str__(self):
        return f'{self.user.nickname} - {self.booth.name} scrap'
    
    
class Show_scrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scrap_user')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='scrap_booth')

    def __str__(self):
        return f'{self.user.nickname} - {self.booth.name} scrap'