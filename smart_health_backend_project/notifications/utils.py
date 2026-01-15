import logging
from django.conf import settings
from .sms_service import send_sms
from .sendgrid_service import send_health_consultation_email

logger = logging.getLogger("notifications")


# --------------------------------------------
# HELPERS
# --------------------------------------------
def resolve_user_name(user):
    if user.get_full_name():
        return user.get_full_name()
    return user.username or user.email or "User"


def resolve_phone(patient):
    """
    Safely resolve phone number from patient or related user
    """
    if hasattr(patient, "phone") and patient.phone:
        return patient.phone
    if hasattr(patient, "user") and hasattr(patient.user, "phone"):
        return patient.user.phone
    return None


# --------------------------------------------
# SAFE SENDGRID EMAIL
# --------------------------------------------
def safe_sendgrid_email(to_email, template_id, dynamic_data):
    try:
        return send_health_consultation_email(
            to_email=to_email,
            dynamic_data=dynamic_data,
            template_id=template_id,
        )
    except Exception as e:
        logger.error(
            f"SendGrid email failed to {to_email} | Template {template_id}: {e}",
            exc_info=True,
        )
        return False


# --------------------------------------------
# SAFE SMS
# --------------------------------------------
def safe_send_sms(phone_number, message):
    if not phone_number:
        logger.warning("SMS skipped: no phone number provided.")
        return False
    try:
        return send_sms(phone_number=phone_number, message=message)
    except Exception as e:
        logger.error(f"SMS failed to {phone_number}: {e}", exc_info=True)
        return False


# --------------------------------------------
# APPOINTMENT BOOKED
# --------------------------------------------
def notify_appointment_booked(patient, doctor, appointment):
    patient_name = resolve_user_name(patient.user)
    doctor_name = resolve_user_name(doctor.user)
    phone = resolve_phone(patient)

    dynamic_data = {
        "patient_name": patient_name,
        "doctor_name": doctor_name,
        "date": str(appointment.date),
        "time": str(appointment.time),
    }

    email_status = safe_sendgrid_email(
        to_email=patient.user.email,
        template_id=settings.SENDGRID_TEMPLATE_APPOINTMENT_BOOKED,
        dynamic_data=dynamic_data,
    )

    sms_status = safe_send_sms(
        phone,
        f"Your appointment with Dr. {doctor_name} "
        f"is booked for {appointment.date} at {appointment.time}.",
    )

    return {"email": email_status, "sms": sms_status}


# --------------------------------------------
# APPOINTMENT CANCELLED
# --------------------------------------------
def notify_appointment_cancelled(patient, appointment):
    patient_name = resolve_user_name(patient.user)
    phone = resolve_phone(patient)

    dynamic_data = {
        "patient_name": patient_name,
        "date": str(appointment.date),
        "time": str(appointment.time),
    }

    email_status = safe_sendgrid_email(
        to_email=patient.user.email,
        template_id=settings.SENDGRID_TEMPLATE_APPOINTMENT_CANCELLED,
        dynamic_data=dynamic_data,
    )

    sms_status = safe_send_sms(
        phone,
        f"Your appointment on {appointment.date} at {appointment.time} has been cancelled.",
    )

    return {"email": email_status, "sms": sms_status}


# --------------------------------------------
# APPOINTMENT RESCHEDULED
# --------------------------------------------
def notify_appointment_rescheduled(patient, doctor, new_appointment):
    patient_name = resolve_user_name(patient.user)
    doctor_name = resolve_user_name(doctor.user)
    phone = resolve_phone(patient)

    dynamic_data = {
        "patient_name": patient_name,
        "doctor_name": doctor_name,
        "new_date": str(new_appointment.date),
        "new_time": str(new_appointment.time),
    }

    email_status = safe_sendgrid_email(
        to_email=patient.user.email,
        template_id=settings.SENDGRID_TEMPLATE_APPOINTMENT_RESCHEDULED,
        dynamic_data=dynamic_data,
    )

    sms_status = safe_send_sms(
        phone,
        f"Your appointment with Dr. {doctor_name} "
        f"has been rescheduled to {new_appointment.date} at {new_appointment.time}.",
    )

    return {"email": email_status, "sms": sms_status}









