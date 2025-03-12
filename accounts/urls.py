from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
        path('signup/', SignUpView.as_view()),
        path('login/', LoginView.as_view()),
        path('duplicate/',DuplicateUsernameView.as_view()),
        #프론트와 중복된 코드
        #path('kakao/', KakaoLoginView.as_view()),
        path('kakao/',KakaoCallbackView.as_view()),
        #path('kakao/signup/', KakaoSignupView.as_view()),
]