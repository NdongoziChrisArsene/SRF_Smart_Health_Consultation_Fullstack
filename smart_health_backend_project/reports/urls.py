from django.urls import path
from .views import (
    GenerateReportView,
    DownloadReportView,
    ReportStatusView,
    AdminAnalyticsView,
)

urlpatterns = [
    path("generate/", GenerateReportView.as_view()),
    path("<int:pk>/download/", DownloadReportView.as_view()),
    path("<int:pk>/status/", ReportStatusView.as_view()),
    path("analytics/", AdminAnalyticsView.as_view()),
]





































# from django.urls import path
# from .views import (
#     GenerateReportView,
#     DownloadReportView,
#     ReportStatusView,
#     AdminAnalyticsView,
# )

# urlpatterns = [
#     path("generate/", GenerateReportView.as_view(), name="generate-report"),
#     path("<int:pk>/download/", DownloadReportView.as_view(), name="download-report"),
#     path("<int:pk>/status/", ReportStatusView.as_view(), name="report-status"),

#     # ✅ NEW: Admin dashboard analytics
#     path("analytics/", AdminAnalyticsView.as_view(), name="admin-analytics"),
# ]






























# from django.urls import path
# from .views import GenerateReportView, DownloadReportView, ReportStatusView

# urlpatterns = [
#     path("generate/", GenerateReportView.as_view(), name="generate-report"),
#     path("<int:pk>/download/", DownloadReportView.as_view(), name="download-report"),
#     path("<int:pk>/status/", ReportStatusView.as_view(), name="report-status"),  # new endpoint
# ]





