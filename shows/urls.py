from django.urls import path
from .views import ShowNoticeView, ShowGuestBookView, ShowPatchView, ShowListView, ShowCountView

app_name = 'shows'

urlpatterns = [
    path('', ShowListView.as_view(), name='show_list'), 
    path('counts',ShowCountView.as_view()),
    path('notices/<int:booth_id>/', ShowNoticeView.as_view(), name='show-notices'),
    path('guestbooks/<int:booth_id>/', ShowGuestBookView.as_view(), name='show-guestbooks'),
    path('<int:booth_id>/', ShowPatchView.as_view(), name='show-detail'),
]