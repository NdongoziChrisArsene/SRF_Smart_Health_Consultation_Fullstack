from django.contrib.auth import get_user_model
from django.db.models import Sum
from datetime import date

from appointments.models import Appointment

try:
    from payments.models import Payment
except ImportError:
    Payment = None

User = get_user_model()


class AnalyticsService:
    @staticmethod
    def appointment_stats(start: date, end: date) -> dict:
        qs = Appointment.objects.all()

        if hasattr(Appointment, "created_at"):
            qs = qs.filter(created_at__range=[start, end])

        return {
            "total": qs.count(),
            "completed": qs.filter(status="completed").count(),
            "cancelled": qs.filter(status="cancelled").count(),
            "pending": qs.filter(status="pending").count(),
        }

    @staticmethod
    def financial_stats(start: date, end: date) -> dict:
        if not Payment:
            return {"total_revenue": 0}

        total = (
            Payment.objects
            .filter(timestamp__range=[start, end])
            .aggregate(total=Sum("amount"))["total"]
            or 0
        )
        return {"total_revenue": total}

    @staticmethod
    def user_activity_stats(start: date, end: date) -> dict:
        return {
            "new_users": User.objects.filter(date_joined__range=[start, end]).count(),
            "active_users": User.objects.filter(last_login__range=[start, end]).count(),
        }

















































# from appointments.models import Appointment
# from payments.models import Payment
# from django.contrib.auth import get_user_model
# from django.db.models import Sum
# from datetime import date

# User = get_user_model()


# class AnalyticsService:
#     @staticmethod
#     def appointment_stats(start: date, end: date) -> dict:
#         qs = Appointment.objects.filter(created_at__range=[start, end])

#         return {
#             "total": qs.count(),
#             "completed": qs.filter(status="completed").count(),
#             "cancelled": qs.filter(status="cancelled").count(),
#             "pending": qs.filter(status="pending").count(),
#         }

#     @staticmethod
#     def financial_stats(start: date, end: date) -> dict:
#         total = (
#             Payment.objects
#             .filter(timestamp__range=[start, end])
#             .aggregate(total=Sum("amount"))["total"]
#             or 0
#         )
#         return {"total_revenue": total}

#     @staticmethod
#     def user_activity_stats(start: date, end: date) -> dict:
#         return {
#             "new_users": User.objects.filter(date_joined__range=[start, end]).count(),
#             "active_users": User.objects.filter(last_login__range=[start, end]).count(),
#         }


















































# from appointments.models import Appointment
# from payments.models import Payment
# from django.contrib.auth import get_user_model
# from django.db.models import Sum
# from datetime import date

# User = get_user_model()


# class AnalyticsService:
#     @staticmethod
#     def appointment_stats(start: date, end: date) -> dict:
#         qs = Appointment.objects.filter(created_at__range=[start, end])
#         return {
#             "total": qs.count(),
#             "completed": qs.filter(status=Appointment.STATUS_COMPLETED).count(),
#             "cancelled": qs.filter(status=Appointment.STATUS_CANCELLED).count(),
#             "pending": qs.filter(status=Appointment.STATUS_PENDING).count(),
#         }

#     @staticmethod
#     def financial_stats(start: date, end: date) -> dict:
#         total = (
#             Payment.objects
#             .filter(timestamp__range=[start, end])
#             .aggregate(total=Sum("amount"))["total"]
#             or 0
#         )
#         return {"total_revenue": total}

#     @staticmethod
#     def user_activity_stats(start: date, end: date) -> dict:
#         return {
#             "new_users": User.objects.filter(date_joined__range=[start, end]).count(),
#             "active_users": User.objects.filter(last_login__range=[start, end]).count(),
#         }
















