from django.urls import path
from .views import *

app_name = 'scrap'

urlpatterns = [
    path('<int:pk>/', BoothScrapView.as_view(), name='booth-scrap'),
]
