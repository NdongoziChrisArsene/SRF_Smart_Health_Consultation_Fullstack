from django.urls import path
from .views import (
    DoctorProfileView,
    AvailabilityListCreateView,
    AvailabilityDetailView, 
    CreateDiagnosisAPIView,
    DoctorDiagnosisHistoryView,
    PatientDiagnosisHistoryView,
    PrescriptionPDFView,
)

urlpatterns = [
    path("profile/", DoctorProfileView.as_view(), name="doctor-profile"),
    path("availability/", AvailabilityListCreateView.as_view(), name="doctor-availability"),
    path("availability/<int:pk>/", AvailabilityDetailView.as_view(), name="doctor-availability-detail"),
    path("diagnosis/create/", CreateDiagnosisAPIView.as_view(), name="create-diagnosis"), 
    path("diagnosis/doctor/history/", DoctorDiagnosisHistoryView.as_view(), name="doctor-diagnosis-history"),
    path("diagnosis/patient/history/", PatientDiagnosisHistoryView.as_view(), name="patient-diagnosis-history"),
    path("prescription/pdf/<int:diagnosis_id>/", PrescriptionPDFView.as_view(), name="prescription-pdf"),
]


























# from django.urls import path
# from .views import (
#     DoctorProfileView,
#     AvailabilityListCreateView,
#     AvailabilityDetailView, 
#     CreateDiagnosisAPIView,
# )

# urlpatterns = [
#     path("profile/", DoctorProfileView.as_view(), name="doctor-profile"),
#     path("availability/", AvailabilityListCreateView.as_view(), name="doctor-availability"),
#     path("availability/<int:pk>/", AvailabilityDetailView.as_view(), name="doctor-availability-detail"),
#     path("diagnosis/create/", CreateDiagnosisAPIView.as_view(), name="create-diagnosis"), 
#     path("diagnosis/doctor/history/", DoctorDiagnosisHistoryView.as_view(), name="doctor-diagnosis-history"),
#     path("diagnosis/patient/history/", PatientDiagnosisHistoryView.as_view(), name="patient-diagnosis-history"),
#     path("prescription/pdf/<int:diagnosis_id>/", PrescriptionPDFView.as_view(), name="prescription-pdf"),
# ]





























# from django.urls import path    
# from .views import DoctorProfileView, AvailabilityListCreateView, AvailabilityDetailView



# urlpatterns = [
#     path('profile/', DoctorProfileView.as_view(), name="doctor-profile"),    
#     path('availability/', AvailabilityListCreateView.as_view(), name="doctor-availability"),  
#     path('availability/<int:pk>/', AvailabilityDetailView.as_view(), name="doctor-availability-detail"),   
# ]