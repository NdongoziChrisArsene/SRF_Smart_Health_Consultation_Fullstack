from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    specialization = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Doctor Profile"
        verbose_name_plural = "Doctor Profiles"

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"


class Availability(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='availability'
    )
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        verbose_name = "Availability"
        verbose_name_plural = "Availabilities"
        unique_together = ('doctor', 'day_of_week', 'start_time')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.doctor.user.username} - {self.day_of_week} ({self.start_time}-{self.end_time})"

    def clean(self):
        """Validate that start_time is before end_time"""
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")


class Diagnosis(models.Model):
    appointment = models.OneToOneField(
        "appointments.Appointment", 
        on_delete=models.CASCADE,
        related_name='diagnosis'
    )
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Diagnosis"
        verbose_name_plural = "Diagnoses"
        ordering = ['-created_at']

    def __str__(self):
        return f"Diagnosis for Appointment #{self.appointment.id}"


class Prescription(models.Model):
    diagnosis = models.ForeignKey(
        Diagnosis,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.medicine_name} - {self.dosage}"
































