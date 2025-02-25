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
    thumbnail = models.TextField(blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    contact = models.CharField(blank=True, max_length=200)
    is_opened = models.BooleanField(default=True)
    is_show = models.BooleanField(default=False)
    scrap_count = models.IntegerField(default=0)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=10)
    show_num = models.IntegerField()
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.category})'

# 공연 일정
class OperatingHours(models.Model):
    DAYOFWEEK_CHOICES = (
        ('수요일', '수요일'),
        ('목요일', '목요일'),
        ('금요일', '금요일'),
    )
    
    DATE_CHOICES = (
        (10, 10),
        (11, 11),
        (12, 12),
    )

    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='schedule')  
    day_of_week = models.CharField(choices=DAYOFWEEK_CHOICES, max_length=5)
    date = models.IntegerField(choices=DATE_CHOICES)
    start_time = models.CharField(max_length=5, null=False)  
    end_time = models.CharField(max_length=5, null=False)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  # 수정일

    def __str__(self):
        return f'{self.show.name} - {self.day_of_week} {self.start_time}~{self.end_time}'
