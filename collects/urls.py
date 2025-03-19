from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'collects'


urlpatterns = [
    path('createbooth/', create_booth, name='create_booth'),
    path('createmenu/', create_menu, name='create_menu'),
]