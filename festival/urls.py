from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path("accounts/", include('accounts.urls')),

    path("booths/", include('booths.urls')),
    # path("shows/", include('shows.urls')),
    # path("notices/", include('notices.urls')),
    # path("mypages/", include('mypages.urls')),
]

