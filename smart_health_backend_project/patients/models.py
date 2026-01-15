from django.db import models
from django.conf import settings


class PatientProfile(models.Model): 
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    blood_group = models.CharField(
        max_length=3, 
        choices=BLOOD_GROUP_CHOICES, 
        blank=True
    )
    allergies = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Patient Profile"
        verbose_name_plural = "Patient Profiles"

    def __str__(self):
        return f"{self.user.username} - Patient Profile"






































