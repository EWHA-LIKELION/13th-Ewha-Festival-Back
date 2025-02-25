from django.db import models
from booths.models import Booth
from shows.models import Show

class Notice(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='booth_notice', null=True, blank=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='show_notice', null=True, blank=True)
    title = models.CharField(max_length=30, null=False)
    content = models.TextField(null=False)
    operating_hours = models.CharField(max_length=100, null=True, blank=True)  # 운영시간 (예: 수목금 10:00 - 18:00)
    contact_info = models.TextField(null=True, blank=True)  # 운영진 연락처
    status = models.CharField(max_length=20, choices=[('운영중', '운영중'), ('운영종료', '운영종료')], default='운영중')  # 운영 여부
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
<<<<<<< HEAD
        if self.booth:
            return f'{self.booth.name} - {self.id} notice'
        elif self.show:
            return f'{self.show.name} - {self.id} notice'
        return f'Notice {self.id}'
=======
        return f'{self.booth.name} - {self.id} notice'
    
class OperationNotice(models.Model):
    title = models.CharField(max_length=22, null=False) #최대 22글자로 제한 
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'운영공지 - {self.title}'
>>>>>>> e9d92ca0af21e2580d458001d9b72b6503462804
