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

        ('잔디광장', '잔디광장'),
        ('아산공학관관', '아산공학관관'),
        ('스포츠트랙 옆', '스포츠트랙 옆'),

        ('학문관 4층 전시실', '학문관 4층 전시실'),
        ('정문 돌담 앞', '정문 돌담 앞'),
        ('학교 전체', '학교 전체'),
        ('ECC B4 삼성홀 앞', 'ECC B4 삼성홀 앞'),

        ('정문03', '정문03'),   
        ('정문02', '정문02'),
        ('스포츠트랙28', '스포츠트랙28'),
        ('학문관 지하', '학문관 지하')

    )

    CATEGORY_CHOICES = (
        # 부스 카테고리
        ('음식', '음식'),
        ('굿즈', '굿즈'),
        ('체험형', '체험형'),

        # 공연 카테고리
        ('댄스', '댄스'),
        ('밴드', '밴드'),
        ('연극', '연극'),
        ('보컬', '보컬')
 
    )

    name = models.CharField(max_length=100)
    thumbnail = models.TextField(blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    contact = models.CharField(blank=True, max_length=200)
    is_opened = models.BooleanField(default=True)
    is_show = models.BooleanField(default=False)
    is_committee = models.BooleanField(default=False) # 축준위 부스
    scrap_count = models.IntegerField(default=0)
    menu_count = models.IntegerField(default=0)
    notice_count = models.IntegerField(default=0)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=150)
    booth_num = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def increase_scrap_count(self):
        """스크랩 개수 증가"""
        self.scrap_count += 1
        self.save(update_fields=['scrap_count'])

    def decrease_scrap_count(self):
        if self.scrap_count > 0:
            self.scrap_count -= 1
            self.save(update_fields=['scrap_count'])

    def increase_menu_count(self):
        self.menu_count += 1
        self.save(update_fields=['menu_count'])

    def decrease_menu_count(self):
        if self.menu_count > 0:
            self.menu_count -= 1
            self.save(update_fields=['menu_count'])

    def increase_notice_count(self):
        self.notice_count += 1
        self.save(update_fields=['notice_count'])

    def decrease_notice_count(self):
        if self.notice_count > 0:
            self.notice_count -= 1
            self.save(update_fields=['notice_count'])

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
        (14, 14),
        (15, 15),
        (16, 16),
    )

    booth = models.ForeignKey(
        Booth, on_delete=models.CASCADE, related_name='operating_hours')
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
    booth = models.ForeignKey(
        Booth, related_name='menu', on_delete=models.CASCADE)
    thumbnail = models.TextField(blank=True)
    name = models.CharField(max_length=18, null=False)
    price = models.IntegerField()
    is_vegan = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.booth.name} - {self.name}'
