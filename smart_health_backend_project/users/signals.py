from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        if instance.role == "patient":
            PatientProfile = apps.get_model("patients", "PatientProfile")
            PatientProfile.objects.get_or_create(user=instance)

        elif instance.role == "doctor":
            DoctorProfile = apps.get_model("doctors", "DoctorProfile")
            DoctorProfile.objects.get_or_create(user=instance)

    except LookupError:
        # App not installed yet — ignore safely
        pass


















































# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.apps import apps
# from .models import User


# @receiver(post_save, sender=User)
# def create_user_profiles(sender, instance, created, **kwargs):
#     if not created:
#         return

#     try:
#         if instance.role == User.ROLE_PATIENT:
#             PatientProfile = apps.get_model("patients", "PatientProfile")
#             PatientProfile.objects.get_or_create(user=instance)

#         elif instance.role == User.ROLE_DOCTOR:
#             DoctorProfile = apps.get_model("doctors", "DoctorProfile")
#             DoctorProfile.objects.get_or_create(user=instance)

#     except LookupError:
#         # App not installed – safely ignore
#         pass




































