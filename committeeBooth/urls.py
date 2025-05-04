from django.urls import path
from django.conf import settings
from .views import *

app_name = 'committeeBooth'


urlpatterns=[
  path('',CommitteeBoothListView.as_view()),
  path('pages/<int:booth_id>/',CommitteeBoothView.as_view()),
  path('<int:booth_id>/', CommitteeBoothPatchView.as_view()),
]
