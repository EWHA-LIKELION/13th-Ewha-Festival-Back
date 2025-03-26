from django.urls import path
from django.conf import settings
from .views import *

app_name = 'booths'

urlpatterns=[
  path('',BoothListView.as_view()),
  path('counts',BoothCountView.as_view()),
  path('notices/<int:booth_id>/', BoothNoticeView.as_view()),
  path('menus/<int:booth_id>/', BoothMenuView.as_view()), 
  path('guestbooks/<int:booth_id>/', BoothGuestBookView.as_view()), 
  path('<int:booth_id>/', BoothPatchView.as_view()),
]