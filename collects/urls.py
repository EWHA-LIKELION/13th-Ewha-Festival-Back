from django.urls import path
from .views import *

app_name = 'collects'


urlpatterns = [
    path('', home, name='home'),  
    path('createbooth/', create_booth, name='create_booth'),
    path('createmenu/', create_menu, name='create_menu'),
    path('list/', booth_list, name='booth_list'),
    path('edit/<int:booth_id>/', edit_booth, name='edit_booth'),
    path('detail/<int:booth_id>/', detail, name='detail'),
    path('editmenu/<int:menu_id>/', edit_menu, name='edit_menu')

]