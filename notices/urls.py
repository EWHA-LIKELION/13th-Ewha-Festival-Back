from django.urls import path
from .views import NoticeListView, NoticeDetailView, NoticeCreateView

app_name = 'notices'

urlpatterns = [
    path('', NoticeListView.as_view(), name='list_create_notices'),  # GET: 목록 조회
    path('create/', NoticeCreateView.as_view(), name='create_notice'),  # POST: 공지 생성
    path('<int:notice_id>/', NoticeDetailView.as_view(), name='retrieve_update_delete_notice'),  # GET: 조회, PUT: 수정, DELETE: 삭제
]
