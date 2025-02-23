from django.urls import path
from django.conf import settings
from .views import *

app_name = 'guestbooks'

urlpatterns=[
    path('create/<int:booth_id>/', GuestBookView.as_view()),
    path('delete/<int:booth_id>/<int:guestbook_id>/', GuestBookDeleteView.as_view()),

]