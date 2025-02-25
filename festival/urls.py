from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include('accounts.urls')),

    path("booths/", include('booths.urls')),
    path("scrap/", include('scrap.urls')),
    # path("shows/", include('shows.urls')),
<<<<<<< HEAD
    # path("notices/", include('notices.urls')),
    path("mypages/", include('mypages.urls')),
    path("search/", include("search.urls")),
=======
    path("notices/", include('notices.urls')),
    # path("mypages/", include('mypages.urls')),
    path("menus/", include('menu.urls')),
    path('guestbooks/', include('guestbooks.urls')),
>>>>>>> e9d92ca0af21e2580d458001d9b72b6503462804
]
