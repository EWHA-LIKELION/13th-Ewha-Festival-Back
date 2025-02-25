from django.db import models
from accounts.models import User
from booths.models import Booth
from shows.models import Show

# Create your models here.
class GuestBook(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='guestbook_author')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='guestbook_booth')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True, blank=True, related_name='guestbook_notice')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.booth:
            return f'{self.booth.name} - {self.id} notice'
        elif self.show:
            return f'{self.show.name} - {self.id} notice'
        return f'Notice {self.id}'
