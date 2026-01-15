from django.urls import path
from .views import ( 
    DoctorListView,                
    AvailabilityListCreateView,
    AvailabilityDetailView, 
    CreateDiagnosisAPIView,
    DoctorDiagnosisHistoryView,
    DoctorRecommendationsView,   
    DoctorDetailView,
    PatientDiagnosisHistoryView,
    PrescriptionPDFView,
)

urlpatterns = [      
    path("", DoctorListView.as_view(), name="doctor-list"),
    path("recommendations/", DoctorRecommendationsView.as_view(), name="doctor-recommendations"),
    path("<int:pk>/", DoctorDetailView.as_view(), name="doctor-detail"),
    path("availability/", AvailabilityListCreateView.as_view(), name="doctor-availability"),
    path("availability/<int:pk>/", AvailabilityDetailView.as_view(), name="doctor-availability-detail"),
    path("diagnosis/create/", CreateDiagnosisAPIView.as_view(), name="create-diagnosis"), 
    path("diagnosis/doctor/history/", DoctorDiagnosisHistoryView.as_view(), name="doctor-diagnosis-history"),
    path("diagnosis/patient/history/", PatientDiagnosisHistoryView.as_view(), name="patient-diagnosis-history"),
    path("prescription/pdf/<int:diagnosis_id>/", PrescriptionPDFView.as_view(), name="prescription-pdf"),
]




















