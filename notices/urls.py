from django.urls import path
from .views import NoticeDetailView, NoticeCreateView
from .views import OperationNoticeView


app_name = 'notices'

urlpatterns = [
    path('<int:booth_id>/', NoticeCreateView.as_view(), name='create_notice'),  # POST: 공지 생성
    path('<int:booth_id>/<int:notice_id>/', NoticeDetailView.as_view(), name='retrieve_update_delete_notice'),  # GET: 조회, PUT: 수정, DELETE: 삭제
    path('tf/', OperationNoticeView.as_view()), 

]
