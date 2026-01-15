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
        # appointment.patient may be a PatientProfile; get underlying user
        patient_obj = instance.appointment.patient
        patient_user = getattr(patient_obj, "user", patient_obj)
        email = getattr(patient_user, "email", None)
        if email:
            try:
                send_mail(
                    subject="New Medical Diagnosis Available",
                    message=f"Diagnosis:\n{instance.diagnosis}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
            except Exception as e:
                logger.error(e)













