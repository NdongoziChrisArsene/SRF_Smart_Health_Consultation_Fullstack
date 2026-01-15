from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import PatientProfile
from .serializers import PatientProfileSerializer
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer


class PatientProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update patient profile
    """
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.patient_profile
        except PatientProfile.DoesNotExist:
            raise NotFound("Patient profile not found. Please contact support.")


class PatientAppointmentsView(generics.ListAPIView):
    """
    List all appointments for the authenticated patient
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            patient_profile = self.request.user.patient_profile
        except PatientProfile.DoesNotExist:
            raise NotFound("Patient profile not found.")
        
        return Appointment.objects.filter(
            patient=patient_profile
        ).select_related('doctor__user').order_by('-date', '-time')





































