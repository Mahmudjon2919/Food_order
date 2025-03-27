from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# DRF YASG (Swagger)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Djoser API",
        default_version="v1",
        description="Djoser bilan autentifikatsiya API'lari",
        contact=openapi.Contact(email="jalilovshoxruh555@email.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),

    # API yo‘llari
    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.restaurants.urls")),
    path("auth/", include("djoser.urls")),  # Djoser autentifikatsiya API
    path("auth/", include("djoser.urls.jwt")),  # JWT autentifikatsiya API

    # Swagger hujjatlar
    path("api/v1/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    # Favicon
    path("favicon.ico/", RedirectView.as_view(url="/static/favicon.ico/", permanent=True)),
]
