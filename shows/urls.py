from django.urls import path
from .views import ShowNoticeView, ShowGuestBookView

app_name = 'shows'

urlpatterns = [
    path('notices/<int:show_id>/', ShowNoticeView.as_view(), name='show-notices'),
    path('guestbooks/<int:show_id>/', ShowGuestBookView.as_view(), name='show-guestbooks'),
]
