from django.db import models
from booths.models import Booth

class CommitteeBooth(Booth):
    TYPE_CHOICE = (
        ('기획', '기획'),
        ('대외협력', '대외협력'),
        ('홍보디자인', '홍보디자인'),
        ('프로모션', '프로모션')
    )

    type = models.CharField(choices=TYPE_CHOICE, max_length=10)