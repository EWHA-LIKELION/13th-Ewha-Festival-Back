from django.contrib import admin
from .models import Show, PerformanceSchedule

# Show 모델 관리
@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'show_num', 'is_opened', 'is_show', 'scrap_count', 'created_at', 'updated_at')
    search_fields = ('name', 'category', 'location', 'contact')
    list_filter = ('category', 'location', 'is_opened', 'is_show')
    ordering = ('created_at',)

# PerformanceSchedule 모델 관리
@admin.register(PerformanceSchedule)
class PerformanceScheduleAdmin(admin.ModelAdmin):
    list_display = ('show', 'day_of_week', 'start_time', 'end_time', 'created_at', 'updated_at')
    search_fields = ('show__name', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    ordering = ('show', 'day_of_week', 'start_time')

