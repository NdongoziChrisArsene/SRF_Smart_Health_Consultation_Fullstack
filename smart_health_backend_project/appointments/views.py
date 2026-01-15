from rest_framework import generics, permissions, filters, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from datetime import timedelta

from users.permissions import IsPatient, IsDoctor
from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    CreateAppointmentSerializer,
    UpdateAppointmentStatusSerializer,
)
from .utils import notify_appointment_booked, notify_appointment_cancelled


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PatientCreateAppointmentView(generics.CreateAPIView):
    serializer_class = CreateAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        patient = getattr(self.request.user, "patient_profile", None)
        if not patient:
            raise NotFound("Patient profile not found.")

        appointment = serializer.save(patient=patient)
        notify_appointment_booked(
            patient=appointment.patient,
            doctor=appointment.doctor,
            appointment=appointment
        )


class PatientAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["doctor__user__username", "reason_for_visit"]
    ordering_fields = ["date", "created_at"]

    def get_queryset(self):
        patient = getattr(self.request.user, "patient_profile", None)
        if not patient:
            raise NotFound("Patient profile not found.")
        return Appointment.objects.filter(patient=patient)


class PatientCancelAppointmentView(generics.UpdateAPIView):
    serializer_class = UpdateAppointmentStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_queryset(self):
        patient = getattr(self.request.user, "patient_profile", None)
        if not patient:
            raise NotFound("Patient profile not found.")
        return Appointment.objects.filter(patient=patient)

    def patch(self, request, *args, **kwargs):
        appointment = self.get_object()
        serializer = self.get_serializer(
            appointment,
            data={"status": Appointment.STATUS_CANCELLED},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        notify_appointment_cancelled(
            patient=appointment.patient,
            appointment=appointment
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        doctor = getattr(self.request.user, "doctor_profile", None)
        if not doctor:
            raise NotFound("Doctor profile not found.")
        return Appointment.objects.filter(doctor=doctor)


class DoctorUpdateAppointmentStatusView(generics.UpdateAPIView):
    serializer_class = UpdateAppointmentStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        doctor = getattr(self.request.user, "doctor_profile", None)
        if not doctor:
            raise NotFound("Doctor profile not found.")
        return Appointment.objects.filter(doctor=doctor)


class AdminAllAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination
    queryset = Appointment.objects.all()


class AdminAppointmentTrendView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        period = request.query_params.get("period", "last_7_days")

        ranges = {
            "today": (today, today),
            "yesterday": (today - timedelta(days=1), today - timedelta(days=1)),
            "last_7_days": (today - timedelta(days=6), today),
            "last_30_days": (today - timedelta(days=29), today),
        }

        if period not in ranges:
            return Response({"detail": "Invalid period"}, status=400)

        start, end = ranges[period]

        qs = Appointment.objects.filter(date__range=[start, end])
        result = {}

        for a in qs:
            result[str(a.date)] = result.get(str(a.date), 0) + 1

        return Response(
            [{"date": d, "count": c} for d, c in sorted(result.items())]
        )


class AdminAppointmentStatusSummaryView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        qs = Appointment.objects.all()
        summary = {
            status: qs.filter(status=status).count()
            for status, _ in Appointment.STATUS_CHOICES
        }
        return Response(summary)




































