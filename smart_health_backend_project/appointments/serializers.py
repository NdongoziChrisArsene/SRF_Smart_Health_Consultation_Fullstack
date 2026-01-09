from rest_framework import serializers
from django.utils import timezone
from datetime import datetime

from .models import Appointment
from doctors.models import Availability


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.user.username", read_only=True)
    doctor_name = serializers.CharField(source="doctor.user.username", read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("patient", "created_at", "updated_at")


class CreateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["doctor", "availability", "date", "time", "reason_for_visit"]

    def validate(self, data):
        request = self.context["request"]
        patient = getattr(request.user, "patient_profile", None)

        if not patient:
            raise serializers.ValidationError("Patient profile not found.")

        appointment_dt = timezone.make_aware(
            datetime.combine(data["date"], data["time"])
        )

        if appointment_dt < timezone.now():
            raise serializers.ValidationError("Cannot book in the past.")

        doctor = data["doctor"]
        day = data["date"].strftime("%A")

        if not Availability.objects.filter(
            doctor=doctor,
            day_of_week=day,
            start_time__lte=data["time"],
            end_time__gt=data["time"]
        ).exists():
            raise serializers.ValidationError("Doctor not available.")

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

















































# from rest_framework import serializers
# from django.utils import timezone
# from datetime import datetime

# from .models import Appointment
# from doctors.models import Availability


# class AppointmentSerializer(serializers.ModelSerializer):
#     patient_name = serializers.CharField(
#         source="patient.user.username", read_only=True
#     )
#     doctor_name = serializers.CharField(
#         source="doctor.user.username", read_only=True
#     )

#     class Meta:
#         model = Appointment
#         fields = [
#             "id",
#             "patient", "patient_name",
#             "doctor", "doctor_name",
#             "availability",
#             "date", "time",
#             "reason_for_visit",
#             "status",
#             "created_at", "updated_at",
#         ]
#         read_only_fields = [
#             "id",
#             "patient",
#             "patient_name",
#             "doctor_name",
#             "created_at",
#             "updated_at",
#         ]


# class CreateAppointmentSerializer(serializers.ModelSerializer):
#     availability = serializers.PrimaryKeyRelatedField(
#         queryset=Availability.objects.all(),
#         required=False
#     )

#     class Meta:
#         model = Appointment
#         fields = ["doctor", "availability", "date", "time", "reason_for_visit"]

#     def validate(self, data):
#         request = self.context.get("request")
#         patient = getattr(request.user, "patient_profile", None)

#         if not patient:
#             raise serializers.ValidationError("Patient profile not found.")

#         appointment_dt = datetime.combine(data["date"], data["time"])
#         appointment_dt = timezone.make_aware(appointment_dt)

#         if appointment_dt < timezone.now():
#             raise serializers.ValidationError("Cannot book an appointment in the past.")

#         doctor = data["doctor"]
#         availability = data.get("availability")

#         if availability:
#             if availability.doctor != doctor:
#                 raise serializers.ValidationError(
#                     "Selected availability does not belong to this doctor."
#                 )

#             if availability.day_of_week != data["date"].strftime("%A"):
#                 raise serializers.ValidationError(
#                     "Availability does not match appointment date."
#                 )

#             if not (
#                 availability.start_time <= data["time"] < availability.end_time
#             ):
#                 raise serializers.ValidationError(
#                     "Appointment time is outside availability range."
#                 )
#         else:
#             day = data["date"].strftime("%A")
#             if not Availability.objects.filter(
#                 doctor=doctor,
#                 day_of_week=day,
#                 start_time__lte=data["time"],
#                 end_time__gt=data["time"]
#             ).exists():
#                 raise serializers.ValidationError(
#                     "Doctor is not available at this time."
#                 )

#         return data


# class UpdateAppointmentStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Appointment
#         fields = ["status"]

#     ALLOWED_TRANSITIONS = {
#         "pending": ["approved", "cancelled"],
#         "approved": ["completed", "cancelled"],
#         "completed": [],
#         "cancelled": [],
#     }

#     def validate_status(self, value):
#         if value not in dict(Appointment.STATUS_CHOICES):
#             raise serializers.ValidationError("Invalid status.")

#         current = self.instance.status
#         allowed = self.ALLOWED_TRANSITIONS.get(current, [])

#         if value not in allowed:
#             raise serializers.ValidationError(
#                 f"Cannot change status from '{current}' to '{value}'."
#             )

#         return value









