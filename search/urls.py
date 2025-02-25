from django.urls import path
from .views import BoothSearchView

urlpatterns = [
    path("booths/", BoothSearchView.as_view(), name="booth-search"),
]
