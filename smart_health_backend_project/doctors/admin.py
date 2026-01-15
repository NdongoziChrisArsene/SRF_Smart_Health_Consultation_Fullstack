from django.contrib import admin
from .models import DoctorProfile, Availability, Diagnosis, Prescription


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "specialization", "location", "years_of_experience", "is_verified", "rating")
    search_fields = ("user__username", "user__email", "specialization", "location")
    list_filter = ("is_verified", "specialization")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("doctor", "day_of_week", "start_time", "end_time")
    list_filter = ("day_of_week",)
    search_fields = ("doctor__user__username",)


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ("id", "appointment", "get_patient", "get_doctor", "created_at")
    search_fields = ("diagnosis", "notes", "appointment__patient__user__username")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [PrescriptionInline]

    def get_patient(self, obj):
        patient = obj.appointment.patient
        user = getattr(patient, 'user', patient)
        return user.get_full_name() or user.username
    get_patient.short_description = "Patient"

    def get_doctor(self, obj):
        doctor = obj.appointment.doctor
        user = getattr(doctor, 'user', doctor)
        return user.get_full_name() or user.username
    get_doctor.short_description = "Doctor"


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "diagnosis", "medicine_name", "dosage", "duration", "created_at")
    search_fields = ("medicine_name", "diagnosis__diagnosis")
    list_filter = ("created_at",)