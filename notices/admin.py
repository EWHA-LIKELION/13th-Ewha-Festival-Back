from django.contrib import admin
from .models import Notice,OperationNotice

admin.site.register(Notice)

@admin.register(OperationNotice)
class OperationNoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    ordering = ('-created_at',)