from django.db import models
from booths.models import Booth
from shows.models import Show

class Notice(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='booth_notice', null=True, blank=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='show_notice', null=True, blank=True)
    title = models.CharField(max_length=30, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.booth:
            return f'{self.booth.name} - {self.id} notice'
        elif self.show:
            return f'{self.show.name} - {self.id} notice'
        return f'Notice {self.id}'
