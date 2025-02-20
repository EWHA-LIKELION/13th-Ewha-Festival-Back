from django.db import models

# 부스
class Booth(models.Model):
    # 선택사항
    LOCATION_CHOICES = (
        # 부스
        ('교육관', '교육관'),
        ('대강당', '대강당'),
        ('신세계관', '신세계관'),
        ('생활관', '생활관'),
        ('정문', '정문'),
        ('포스코관', '포스코관'),
        ('학문관', '학문관'),
        ('휴웃길', '휴웃길'),
        ('학관', '학관'),

        # 공연
        ('학문관무대', '학문관무대'),
        ('스포츠트랙', '스포츠트랙'),
    )

    CATEGORY_CHOICES = (
        # 부스 카테고리
        ('음식', '음식'),
        ('굿즈', '굿즈'),

        # 공연 카테고리
        ('댄스', '댄스'),
        ('밴드', '밴드')
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
    booth_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# 운영 시간
class OperatingHours(models.Model):
    # 요일
    DAYOFWEEK_CHOICES = (
        ('수요일', '수요일'),
        ('목요일', '목요일'),
        ('금요일', '금요일'),
    )

    # 날짜
    DATE_CHOICES = (
        (10, 10),
        (11, 11),
        (12, 12),
    )

    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='operating_hours')
    day_of_week = models.CharField(choices=DAYOFWEEK_CHOICES, max_length=5)
    date = models.IntegerField(choices=DATE_CHOICES)
    open_time = models.CharField(max_length=5, null=False)
    close_time = models.CharField(max_length=5, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.date}일 {self.day_of_week} {self.open_time}~{self.close_time}'

# 메뉴
class Menu(models.Model):
    booth = models.ForeignKey(Booth, related_name='menu', on_delete=models.CASCADE)
    thumbnail = models.TextField(blank=True)
    name = models.CharField(max_length=18, null=False)
    price = models.IntegerField()
    is_vegan = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.booth.name} - {self.name}'
    
