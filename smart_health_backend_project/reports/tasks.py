# from celery import shared_task
# from django.core.files.base import ContentFile
# from django.core.mail import EmailMessage
# from django.utils import timezone

# from .models import Report


# @shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
# def generate_report_task(self, report_id, report_type, start_date, end_date, email):
#     report = Report.objects.get(id=report_id)

#     # Simulated report content (replace later with real CSV/PDF)
#     content = (
#         f"Report type: {report_type}\n"
#         f"From: {start_date}\n"
#         f"To: {end_date}\n"
#         f"Generated at: {timezone.now()}\n"
#     )

#     report.file.save(
#         f"{report_type}_report_{report_id}.txt",
#         ContentFile(content.encode("utf-8")),
#     )

#     report.is_ready = True
#     report.save(update_fields=["file", "is_ready"])

#     if email:
#         msg = EmailMessage(
#             subject="Your report is ready",
#             body="Please find your report attached.",
#             to=[email],
#         )
#         msg.attach(report.file.name, report.file.read())
#         msg.send()








# reports/tasks.py
import logging
from celery import shared_task
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings

from .models import Report

logger = logging.getLogger("reports")

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def generate_report_task(self, report_id, report_type, start_date, end_date, email=None):
    """
    Generates a report and optionally sends it via email.
    Safe, idempotent, and retries on failure.
    """
    try:
        report = Report.objects.get(id=report_id)

        # Simulated report content (replace with real CSV/PDF generation later)
        content = (
            f"Report type: {report_type}\n"
            f"From: {start_date}\n"
            f"To: {end_date}\n"
            f"Generated at: {timezone.now()}\n"
        )

        # Save report content to file field
        filename = f"{report_type}_report_{report_id}.txt"
        report.file.save(filename, ContentFile(content.encode("utf-8")), save=False)
        report.is_ready = True
        report.save(update_fields=["file", "is_ready"])

        # Send email if provided
        if email:
            try:
                msg = EmailMessage(
                    subject="Your report is ready",
                    body="Please find your report attached.",
                    to=[email],
                )
                # Reset file pointer before attaching
                report.file.open(mode="rb")
                msg.attach(report.file.name, report.file.read())
                report.file.close()
                msg.send()
                logger.info(f"Report {report_id} sent to {email}")
            except Exception as e:
                logger.error(f"Failed to send report {report_id} to {email}: {e}")

        return f"Report {report_id} generated successfully."

    except Report.DoesNotExist:
        logger.error(f"Report with id {report_id} does not exist.")
        return f"Report {report_id} not found."

    except Exception as e:
        logger.exception(f"Error generating report {report_id}")
        raise self.retry(exc=e)






























# from celery import shared_task
# from django.core.mail import EmailMessage
# from .models import Report
# from .services.analytics_service import AnalyticsService
# from .services.report_generator import ReportGenerator


# @shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
# def generate_report_task(self, report_id, report_type, start_date, end_date, email):
#     report = Report.objects.get(id=report_id)

#     service_map = {
#         "appointments": (
#             AnalyticsService.appointment_stats,
#             "reporting/report_summary.html",
#         ),
#         "finance": (
#             AnalyticsService.financial_stats,
#             "reporting/financial_report.html",
#         ),
#         "activity": (
#             AnalyticsService.user_activity_stats,
#             "reporting/user_activity_report.html",
#         ),
#     }

#     analytics_func, template = service_map[report_type]
#     data = analytics_func(start_date, end_date)

#     pdf_file = ReportGenerator.generate_pdf(
#         template=template,
#         context={**data, "start_date": start_date, "end_date": end_date},
#     )
#     pdf_file.name = f"{report_type}_report.pdf"

#     report.file.save(pdf_file.name, pdf_file)
#     report.is_ready = True
#     report.save()

#     # 📧 Email report (SAFE)
#     email_msg = EmailMessage(
#         subject="Your Report Is Ready",
#         body="Please find your generated report attached.",
#         to=[email],
#     )
#     email_msg.attach_file(report.file.path)
#     email_msg.send()








