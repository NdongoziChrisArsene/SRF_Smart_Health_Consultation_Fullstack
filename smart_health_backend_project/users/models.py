from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ("patient", "Patient"),
        ("doctor", "Doctor"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="patient")
    specialization = models.CharField(max_length=100, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email















































































# # users/models.py
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db import models


# class UserManager(BaseUserManager):
#     """Custom user manager"""
    
#     def create_user(self, username, email, password=None, **extra_fields):
#         """Create and return a regular user"""
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not username:
#             raise ValueError('Users must have a username')

#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         """Create and return a superuser"""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('role', 'admin')

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(username, email, password, **extra_fields)


# class User(AbstractUser):
#     """Custom User model"""
    
#     ROLE_CHOICES = [
#         ('patient', 'Patient'),
#         ('doctor', 'Doctor'),
#         ('admin', 'Admin'),
#     ]

#     # Use email as the primary identifier
#     email = models.EmailField(unique=True, max_length=255)
    
#     # Role field
#     role = models.CharField(
#         max_length=10,
#         choices=ROLE_CHOICES,
#         default='patient'
#     )
    
#     # Additional fields
#     phone_number = models.CharField(max_length=20, blank=True, null=True)
#     specialization = models.CharField(max_length=100, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     profile_picture = models.ImageField(
#         upload_to='profile_pics/',
#         blank=True,
#         null=True
#     )
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = UserManager()

#     # Use email for authentication
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']  # Required when creating superuser

#     class Meta:
#         db_table = 'users_user'
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"{self.email} ({self.role})"

#     @property
#     def full_name(self):
#         """Return user's full name"""
#         return f"{self.first_name} {self.last_name}".strip() or self.username

#     def is_doctor(self):
#         """Check if user is a doctor"""
#         return self.role == 'doctor'

#     def is_patient(self):
#         """Check if user is a patient"""
#         return self.role == 'patient'

#     def is_admin(self):
#         """Check if user is an admin"""
#         return self.role == 'admin'  