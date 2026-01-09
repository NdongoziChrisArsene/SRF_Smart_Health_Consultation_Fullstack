from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Diagnosis
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Diagnosis)
def notify_patient_on_diagnosis(sender, instance, created, **kwargs):
    if created:
        patient = instance.appointment.patient
        if patient.email:
            try:
                send_mail(
                    subject="New Medical Diagnosis Available",
                    message=f"Diagnosis:\n{instance.diagnosis}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[patient.email],
                )
            except Exception as e:
                logger.error(e)

























































# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import User
# from .models import DoctorProfile, Diagnosis
# from django.core.mail import send_mail
# from django.conf import settings
# import logging

# logger = logging.getLogger(__name__)


# @receiver(post_save, sender=Diagnosis)
# def notify_patient_on_diagnosis(sender, instance, created, **kwargs):
#     """
#     Send email notification to patient when a new diagnosis is created.
#     """
#     if created:
#         patient = getattr(instance.appointment, "patient", None)
#         if patient and patient.email:
#             try:
#                 send_mail(
#                     subject="New Medical Diagnosis Available",
#                     message=f"Your diagnosis has been added:\n\n{instance.diagnosis}",
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[patient.email],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 logger.error(f"Failed to send diagnosis email to {patient.email}: {e}")









































# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import User
# from .models import DoctorProfile, Diagnosis
# from django.core.mail import send_mail 
# from django.conf import settings 



# @receiver(post_save, sender=User)
# def create_doctor_profile(sender, instance, created, **kwargs):
#     """
#     Auto-create DoctorProfile when a doctor user is created.
#     """
#     if created and getattr(instance, "role", None) == "doctor":
#         DoctorProfile.objects.get_or_create(user=instance)

# @receiver(post_save, sender=Diagnosis)
# def notify_patient_on_diagnosis(sender, instance, created, **kwargs):
#     if created:
#         patient = instance.appointment.patient
#         send_mail(
#             subject="New Medical Diagnosis Available",
#             message=f"Your diagnosis has been added:\n\n{instance.diagnosis}",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[patient.email],
#             fail_silently=True,
#         )


























# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import User
# from .models import DoctorProfile


# @receiver(post_save, sender=User)
# def create_doctor_profile(sender, instance, created, **kwargs):
#     """
#     Automatically creates a Doctor profile ONLY when:
#     - A new User is created
#     - User.role == 'doctor'
#     """
#     if created and getattr(instance, "role", None) == "doctor":
#         DoctorProfile.objects.get_or_create(user=instance)
