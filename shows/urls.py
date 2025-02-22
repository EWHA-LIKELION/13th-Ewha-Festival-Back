from django.urls import path
from .views import ShowNoticeView, ShowGuestBookView, ShowPatchView

app_name = 'shows'

urlpatterns = [
    path('notices/<int:show_id>/', ShowNoticeView.as_view(), name='show-notices'),
    path('guestbooks/<int:show_id>/', ShowGuestBookView.as_view(), name='show-guestbooks'),
    path('shows/<int:show_id>/', ShowPatchView.as_view(), name='show-detail'),
]