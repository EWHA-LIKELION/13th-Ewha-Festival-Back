from django.db import models
from booths.models import Booth
from accounts.models import User

class Notice(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='booth_notice', null=True, blank=True)
    title = models.CharField(max_length=30, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # booth가 None이면 show의 이름을 사용, booth가 있으면 booth.name 사용
        if self.booth:
            return f'{self.booth.name} - {self.id} notice'
        else:
            return f'No Booth or Show - {self.id} notice'
        
class OperationNotice(models.Model):
    title = models.CharField(max_length=30, null=False) #최대 30글자로 제한 
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'운영공지 - {self.title}'
