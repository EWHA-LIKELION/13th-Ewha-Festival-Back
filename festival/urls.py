from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg       import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ewha-festival",
        default_version='1.0',
        description="이화 대동제 API 문서",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # swagger
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    
    path('admin/', admin.site.urls),
    path("accounts/", include('accounts.urls')),

    path("booths/", include('booths.urls')),
    path("shows/", include('shows.urls')),
    path("notices/", include('notices.urls')),
    # path("mypages/", include('mypages.urls')),
]

