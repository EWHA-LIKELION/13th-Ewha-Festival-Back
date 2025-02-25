from django.urls import path
from django.conf import settings
from .views import *

app_name = 'menu'

urlpatterns=[
    path('<int:booth_id>/', MenuView.as_view()),
    path('<int:booth_id>/<int:menu_id>/', MenuPatchView.as_view()),
]