from django.urls import path
from .views import OperationNoticeView

app_name = 'notices'

urlpatterns = [
    path('tf/', OperationNoticeView.as_view()), 
]
