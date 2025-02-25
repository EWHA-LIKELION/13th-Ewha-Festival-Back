from django.urls import path
<<<<<<< HEAD
from .views import NoticeListView, NoticeDetailView
=======
from .views import OperationNoticeView
>>>>>>> e9d92ca0af21e2580d458001d9b72b6503462804

app_name = 'notices'

urlpatterns = [
<<<<<<< HEAD
    path('', NoticeListView.as_view(), name='list_create_notices'),  # GET: 목록 조회, POST: 공지 생성
    path('<int:notice_id>/', NoticeDetailView.as_view(), name='retrieve_update_delete_notice'),  # GET: 조회, PUT: 수정, DELETE: 삭제
]
=======
    path('tf/', OperationNoticeView.as_view()), 
]
>>>>>>> e9d92ca0af21e2580d458001d9b72b6503462804
