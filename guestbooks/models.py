from django.db import models
from accounts.models import User
from booths.models import Booth

# Create your models here.
class GuestBook(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='guestbook_author')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='guestbook_booth')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    #방명록 수정 기능이 없으므로 삭제
    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.booth.name} guestbook'
