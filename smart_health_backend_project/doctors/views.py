from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response

from .models import DoctorProfile, Availability, Diagnosis
from .serializers import AvailabilitySerializer, DiagnosisSerializer, DoctorProfileSerializer
from users.permissions import IsDoctor, IsPatient


class DoctorListView(generics.ListAPIView):
    """
    List all verified doctors
    """
    queryset = DoctorProfile.objects.filter(
        is_verified=True
    ).select_related('user').prefetch_related('availability').order_by('-years_of_experience')
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorRecommendationsView(generics.ListAPIView):
    """
    Get recommended doctors (top 10 by experience)
    """
    queryset = DoctorProfile.objects.filter(
        is_verified=True
    ).select_related('user').prefetch_related('availability').order_by('-years_of_experience')[:10]
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorDetailView(generics.RetrieveAPIView):
    """
    Get single doctor details
    """
    queryset = DoctorProfile.objects.filter(is_verified=True).select_related('user').prefetch_related('availability')
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class AvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Availability.objects.filter(doctor=self.request.user.doctor_profile)

    def perform_create(self, serializer):
        instance = serializer.save(doctor=self.request.user.doctor_profile)
        try:
            instance.full_clean()
        except ValidationError as e:
            from rest_framework.exceptions import ValidationError as DRFValidationError
            raise DRFValidationError(detail=e.message_dict or e.messages)
        instance.save()


class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Availability.objects.filter(doctor=self.request.user.doctor_profile)


class CreateDiagnosisAPIView(generics.CreateAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        appointment = serializer.validated_data["appointment"]

        # Get the doctor user from appointment
        doctor_user = getattr(appointment.doctor, "user", appointment.doctor)
        if doctor_user != self.request.user:
            raise PermissionDenied("You are not assigned to this appointment.")

        serializer.save()


class DoctorDiagnosisHistoryView(generics.ListAPIView):
    """
    View for doctors to see all diagnoses they've created
    """
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # Get doctor profile
        doctor_profile = getattr(self.request.user, 'doctor_profile', None)
        if not doctor_profile:
            return Diagnosis.objects.none()
        
        return Diagnosis.objects.filter(
            appointment__doctor=doctor_profile
        ).select_related('appointment__patient__user').prefetch_related('prescriptions').order_by('-created_at')


class PatientDiagnosisHistoryView(generics.ListAPIView):
    """
    View for patients to see their own diagnosis history
    """
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get_queryset(self):
        # Get patient profile
        patient_profile = getattr(self.request.user, 'patient_profile', None)
        if not patient_profile:
            return Diagnosis.objects.none()
        
        return Diagnosis.objects.filter(
            appointment__patient=patient_profile
        ).select_related('appointment__doctor__user').prefetch_related('prescriptions').order_by('-created_at')


class PrescriptionPDFView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, diagnosis_id):
        diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)

        # Normalize to underlying user objects for comparison
        doctor_user = getattr(diagnosis.appointment.doctor, "user", diagnosis.appointment.doctor)
        patient_user = getattr(diagnosis.appointment.patient, "user", diagnosis.appointment.patient)

        if doctor_user != request.user and patient_user != request.user:
            raise PermissionDenied("Not allowed")

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="prescription.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 800, "Medical Prescription")
        p.drawString(100, 770, f"Patient: {patient_user.get_full_name() or patient_user.username}")
        p.drawString(100, 740, f"Doctor: {doctor_user.get_full_name() or doctor_user.username}")
        p.drawString(100, 710, f"Date: {diagnosis.created_at.strftime('%Y-%m-%d')}")
        p.drawString(100, 680, f"Diagnosis: {diagnosis.diagnosis}")
        p.drawString(100, 650, f"Notes: {diagnosis.notes}")

        y = 610
        p.drawString(100, y, "Prescriptions:")
        y -= 30
        
        for pres in diagnosis.prescriptions.all():
            p.drawString(
                120, y,
                f"• {pres.medicine_name} - {pres.dosage} - {pres.duration}"
            )
            y -= 25

        p.showPage()
        p.save()
        return response
















