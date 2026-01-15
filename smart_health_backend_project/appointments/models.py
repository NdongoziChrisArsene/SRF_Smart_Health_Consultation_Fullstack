from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

# Use string references for related models to avoid circular imports
# patient -> 'patients.PatientProfile'
# doctor -> 'doctors.DoctorProfile'
# availability -> 'doctors.Availability'


class Appointment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_COMPLETED, "Completed"),
    )

    patient = models.ForeignKey(
        "patients.PatientProfile",
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    doctor = models.ForeignKey(
        "doctors.DoctorProfile",
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    availability = models.ForeignKey(
        "doctors.Availability",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="appointments"
    )

    date = models.DateField()
    time = models.TimeField()
    reason_for_visit = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = (
            ("doctor", "date", "time"),
            ("patient", "date", "time"),
        )

    def clean(self):
        appointment_dt = datetime.combine(self.date, self.time)
        appointment_dt = timezone.make_aware(appointment_dt)

        if appointment_dt < timezone.now():
            raise ValidationError("Cannot book appointment in the past.")

        if self.availability:
            if self.availability.doctor != self.doctor:
                raise ValidationError("Availability does not belong to doctor.")

            if self.availability.day_of_week != self.date.strftime("%A"):
                raise ValidationError("Availability does not match date.")

            if not (
                self.availability.start_time <= self.time < self.availability.end_time
            ):
                raise ValidationError("Time outside availability window.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.user.username} → {self.doctor.user.username}"











