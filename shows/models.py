from django.db import models

class Category(models.Model):
    CATEGORY_CHOICES = (
        ('밴드', '밴드'),
        ('댄스', '댄스'),
    )
    name = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.get_name_display()

class Location(models.Model):
    LOCATION_CHOICES = (
        ('학문관 광장','학문관 광장'),
        ('스포츠 트랙','스포츠 트랙'),
    )
    name = models.CharField(max_length=20, choices=LOCATION_CHOICES)

    def __str__(self):
        return self.get_name_display()
    
class Day(models.Model):
    DAY_CHOICES = (
        ('수요일', '수'),
        ('목요일', '목'),
        ('금요일', '금'),
    )

    name = models.CharField(max_length=10, choices = DAY_CHOICES)

    def __str__(self):
        return self.get_name_display()
    

class Show(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    time = models.TimeField()

    def __str__(self):
        return self.title
    
