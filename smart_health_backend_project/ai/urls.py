from django.urls import path
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi 

from .views import (
    AISymptomCheckerView,
    AIMedicalSummaryView,
    AIDoctorRecommendationView,
    AdminAIInsightsView
)

app_name = "ai_api"

schema_view = get_schema_view(
    openapi.Info(
        title="AI Health API",
        default_version="v1",
        description="Endpoints for AI-powered symptom checking, medical summaries, and doctor recommendations.",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Match frontend expectations
    path("check-symptoms/", AISymptomCheckerView.as_view(), name="check_symptoms"),
    path("recommend-doctors/", AIDoctorRecommendationView.as_view(), name="recommend_doctors"),
    path("medical/summary/", AIMedicalSummaryView.as_view(), name="medical_summary"),
    path("admin/insights/", AdminAIInsightsView.as_view(), name="admin_insights"),
    
    # Keep v1 endpoints for backward compatibility
    path("v1/symptoms/checker/", AISymptomCheckerView.as_view(), name="v1_symptom_checker"),
    path("v1/medical/summary/", AIMedicalSummaryView.as_view(), name="v1_medical_summary"),
    path("v1/doctors/recommendation/", AIDoctorRecommendationView.as_view(), name="v1_doctor_recommendation"),
    path("v1/admin/insights/", AdminAIInsightsView.as_view(), name="v1_admin_insights"),
]

if settings.DEBUG:
    urlpatterns += [
        path("v1/docs/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
        path("v1/docs/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
    ]











