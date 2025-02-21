from django.db import models
from booths.models import Booth

class Notice(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='booth_notice')
    title = models.CharField(max_length=30, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.booth.name} - {self.id} notice'