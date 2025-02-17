from django.contrib import admin
from .models import Category, Location, Day, Show
# Register your models here.

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Day)
admin.site.register(Show)