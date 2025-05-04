from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
        path('signup/', SignUpView.as_view()),
        path('login/', LoginView.as_view()),
        path('duplicate/',DuplicateUsernameView.as_view()),
        path('kakao/prod', KakaoProdCallbackView.as_view()),
        path('kakao/dev', KakaoDevCallbackView.as_view()),
        path('refresh/', CustomTokenRefreshView.as_view()),
]