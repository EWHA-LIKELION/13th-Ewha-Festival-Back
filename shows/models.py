from django.db import models

# 공연 정보
class Show(models.Model):
    CATEGORY_CHOICES = (
        ('댄스', '댄스'),
        ('밴드', '밴드'),
    )

    LOCATION_CHOICES = (
        ('학문관무대', '학문관무대'),
        ('스포츠트랙', '스포츠트랙'),
    )

    name = models.CharField(max_length=100) 
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10) 
    location = models.CharField(choices=LOCATION_CHOICES, max_length=10)  
    description = models.TextField(blank=True)  
    contact = models.CharField(blank=True, max_length=200) 
    thumbnail = models.TextField(blank=True)  # 
    scrap_count = models.IntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f'{self.name} ({self.category})'

# 공연 일정
class PerformanceSchedule(models.Model):
    DAYOFWEEK_CHOICES = (
        ('수요일', '수요일'),
        ('목요일', '목요일'),
        ('금요일', '금요일'),
    )

    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='schedule')  
    day_of_week = models.CharField(choices=DAYOFWEEK_CHOICES, max_length=5) 
    start_time = models.CharField(max_length=5, null=False)  
    end_time = models.CharField(max_length=5, null=False)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.show.name} - {self.day_of_week} {self.start_time}~{self.end_time}'
