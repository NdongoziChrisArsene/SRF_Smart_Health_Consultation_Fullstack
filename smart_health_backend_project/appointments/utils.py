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

















































# import logging
# import asyncio

# logger = logging.getLogger(__name__)


# async def async_notify(message):
#     await asyncio.sleep(0.1)
#     logger.info(message)


# def notify_appointment_booked(patient, doctor, appointment):
#     try:
#         msg = (
#             f"[BOOKED] Patient={patient.user.username}, "
#             f"Doctor={doctor.user.username}, "
#             f"Date={appointment.date}, Time={appointment.time}"
#         )
#         asyncio.run(async_notify(msg))
#         return True
#     except Exception as e:
#         logger.error(f"Notify booked failed: {e}")
#         return False


# def notify_appointment_cancelled(patient, appointment):
#     try:
#         msg = (
#             f"[CANCELLED] Patient={patient.user.username}, "
#             f"Date={appointment.date}, Time={appointment.time}"
#         )
#         asyncio.run(async_notify(msg))
#         return True
#     except Exception as e:
#         logger.error(f"Notify cancelled failed: {e}")
#         return False










