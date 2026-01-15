from django.urls import path
from .views import (
    PatientProfileView,
    PatientAppointmentsView,
)

app_name = 'patients'

urlpatterns = [
    path("profile/", PatientProfileView.as_view(), name="patient-profile"),
    path("appointments/", PatientAppointmentsView.as_view(), name="patient-appointments"),
]
