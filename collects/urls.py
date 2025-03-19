from django.urls import path
from .views import *

app_name = 'collects'


urlpatterns = [
    path('createbooth/', create_booth, name='create_booth'),
    path('createmenu/', create_menu, name='create_menu'),
]