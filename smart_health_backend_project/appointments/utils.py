import logging

logger = logging.getLogger(__name__)


def notify_appointment_booked(patient, doctor, appointment):
    logger.info(
        f"[BOOKED] Patient={patient.user.username}, "
        f"Doctor={doctor.user.username}, "
        f"{appointment.date} {appointment.time}"
    )


def notify_appointment_cancelled(patient, appointment):
    logger.info(
        f"[CANCELLED] Patient={patient.user.username}, "
        f"{appointment.date} {appointment.time}"
    )








