from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, time as dt_time

from .models import Appointment
from doctors.models import Availability


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.user.username", read_only=True)
    doctor_name = serializers.CharField(source="doctor.user.username", read_only=True)
    doctor_specialization = serializers.CharField(source="doctor.specialization", read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("patient", "created_at", "updated_at")


class CreateAppointmentSerializer(serializers.ModelSerializer):
    # Accept scheduled_at from frontend
    scheduled_at = serializers.DateTimeField(write_only=True, required=False)
    
    class Meta:
        model = Appointment
        fields = ["doctor", "availability", "date", "time", "reason_for_visit", "scheduled_at"]
        extra_kwargs = {
            'date': {'required': False},
            'time': {'required': False},
            'availability': {'required': False}
        }

    def validate(self, data):
        request = self.context["request"]
        patient = getattr(request.user, "patient_profile", None)

        if not patient:
            raise serializers.ValidationError("Patient profile not found.")

        # Handle scheduled_at from frontend
        if 'scheduled_at' in data:
            scheduled_dt = data['scheduled_at']
            if timezone.is_naive(scheduled_dt):
                scheduled_dt = timezone.make_aware(scheduled_dt)
            
            data['date'] = scheduled_dt.date()
            data['time'] = scheduled_dt.time()
        
        # Ensure we have date and time
        if 'date' not in data or 'time' not in data:
            raise serializers.ValidationError("Date and time are required.")

        # Validate not in past
        appointment_dt = timezone.make_aware(
            datetime.combine(data["date"], data["time"])
        )

        if appointment_dt < timezone.now():
            raise serializers.ValidationError("Cannot book appointments in the past.")

        doctor = data["doctor"]
        day = data["date"].strftime("%A")

        # Check doctor availability
        if not Availability.objects.filter(
            doctor=doctor,
            day_of_week=day,
            start_time__lte=data["time"],
            end_time__gt=data["time"]
        ).exists():
            raise serializers.ValidationError(
                f"Doctor is not available on {day} at {data['time']}. "
                "Please check their availability schedule."
            )

        # Check for conflicts
        if Appointment.objects.filter(
            doctor=doctor,
            date=data["date"],
            time=data["time"]
        ).exclude(status=Appointment.STATUS_CANCELLED).exists():
            raise serializers.ValidationError(
                "This time slot is already booked. Please choose another time."
            )

        return data


class UpdateAppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["status"]

    ALLOWED_TRANSITIONS = {
        "pending": ["approved", "cancelled"],
        "approved": ["completed", "cancelled"],
        "completed": [],
        "cancelled": [],
    }

    def validate_status(self, value):
        current = self.instance.status
        if value not in self.ALLOWED_TRANSITIONS[current]:
            raise serializers.ValidationError(
                f"Cannot change status from {current} to {value}"
            )
        return value







