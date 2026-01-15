from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger / Redoc
schema_view = get_schema_view(
    openapi.Info(
        title="Smart Health System API",
        default_version="v1",
        description="API documentation for Smart Health Backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Core URLs
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/doctors/", include("doctors.urls")),
    path("api/appointments/", include("appointments.urls")),
    path("api/", include("ai.urls")),
    path("api/reports/", include("reports.urls")),
]

# API Docs (DEBUG ONLY)
if settings.DEBUG:
    urlpatterns += [
        path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]








































