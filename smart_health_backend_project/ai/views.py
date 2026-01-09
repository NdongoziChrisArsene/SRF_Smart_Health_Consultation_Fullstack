from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from rest_framework.permissions import IsAdminUser

from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate

from appointments.models import Appointment
from doctors.models import DoctorProfile

from datetime import timedelta
import logging

from .serializers import (
    SymptomCheckerSerializer,
    MedicalSummarySerializer,
    DoctorRecommendationSerializer,
    AdminAIInsightsSerializer,
)
from .gemini_utils import call_gemini

from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger("ai")


# -----------------------------
# Base AI View
# -----------------------------
class BaseAIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "ai"
    http_method_names = ["post"]

    def format_response(self, data=None, message="", status_type="success",
                        http_status=status.HTTP_200_OK):
        return Response(
            {"status": status_type, "message": message, "data": data},
            status=http_status
        )


# -----------------------------
# 1. AI Symptom Checker
# -----------------------------
class AISymptomCheckerView(BaseAIView):
    serializer_class = SymptomCheckerSerializer

    @swagger_auto_schema(
        operation_summary="AI Symptom Checker",
        request_body=SymptomCheckerSerializer
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = call_gemini(
            f"Analyze these symptoms medically and safely: {serializer.validated_data['symptoms']}"
        )

        return self.format_response(
            data={"analysis": result},
            message="Symptom analysis completed."
        )


# -----------------------------
# 2. AI Medical Summary
# -----------------------------
class AIMedicalSummaryView(BaseAIView):
    serializer_class = MedicalSummarySerializer

    @swagger_auto_schema(
        operation_summary="AI Medical Summary",
        request_body=MedicalSummarySerializer
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        summary = call_gemini(
            f"Generate a professional medical summary: {serializer.validated_data['medical_history']}"
        )

        return self.format_response(
            data={"summary": summary},
            message="Medical summary generated."
        )


# -----------------------------
# 3. AI Doctor Recommendation
# -----------------------------
class AIDoctorRecommendationView(BaseAIView):
    serializer_class = DoctorRecommendationSerializer

    @swagger_auto_schema(
        operation_summary="AI Doctor Recommendation",
        request_body=DoctorRecommendationSerializer
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        symptoms = serializer.validated_data["symptoms"]
        location = serializer.validated_data["location"]

        doctors = DoctorProfile.objects.select_related("user").filter(
            location__icontains=location,
            is_verified=True
        )

        if not doctors.exists():
            return self.format_response(
                data=[],
                message="No verified doctors found in this location.",
                status_type="error",
                http_status=status.HTTP_404_NOT_FOUND
            )

        doctor_names = [doc.user.get_full_name() or doc.user.username for doc in doctors]

        recommendation = call_gemini(
            f"Recommend the best doctors for symptoms '{symptoms}' "
            f"from this list: {doctor_names}"
        )

        return self.format_response(
            data={"recommendation": recommendation},
            message="Doctor recommendation generated."
        )


# -----------------------------
# 4. Admin AI Insights
# -----------------------------
class AdminAIInsightsView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Admin AI Insights",
        request_body=AdminAIInsightsSerializer
    )
    def post(self, request):
        serializer = AdminAIInsightsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        end_date = serializer.validated_data.get(
            "end_date", timezone.now().date()
        )
        start_date = serializer.validated_data.get(
            "start_date", end_date - timedelta(days=30)
        )

        # Top doctors
        top_doctors = (
            Appointment.objects
            .filter(date__range=[start_date, end_date])
            .values("doctor__user__username")
            .annotate(total_appointments=Count("id"))
            .order_by("-total_appointments")[:5]
        )

        # Appointment trends
        trend_data = (
            Appointment.objects
            .filter(date__range=[start_date, end_date])
            .annotate(day=TruncDate("date"))
            .values("day")
            .annotate(total=Count("id"))
            .order_by("day")
        )

        # High-risk patients
        high_risk_patients = (
            Appointment.objects
            .filter(
                date__range=[start_date, end_date],
                status=Appointment.STATUS_CANCELLED
            )
            .values("patient__user__username")
            .annotate(cancelled_count=Count("id"))
            .order_by("-cancelled_count")[:5]
        )

        insight_text = call_gemini(
            f"Summarize these appointment trends for a hospital admin: {list(trend_data)}"
        )

        return Response({
            "top_doctors": list(top_doctors),
            "appointment_trend": list(trend_data),
            "high_risk_patients": list(high_risk_patients),
            "ai_summary": insight_text
        })





































































# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
# from rest_framework.permissions import IsAdminUser
# from appointments.models import Appointment
# from users.models import User
# from django.db.models import Count
# from datetime import datetime, timedelta
# from .gemini_utils import call_gemini
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# import logging

# from .serializers import (
#     SymptomCheckerSerializer,
#     MedicalSummarySerializer,
#     DoctorRecommendationSerializer,
#     AdminAIInsightsSerializer,  # ✅ Import the new serializer
# )
# from doctors.models import DoctorProfile

# logger = logging.getLogger("ai")


# # -----------------------------
# # Base AI View
# # -----------------------------
# class BaseAIView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     throttle_classes = [UserRateThrottle, ScopedRateThrottle]
#     throttle_scope = "ai"
#     http_method_names = ["post"]

#     def format_response(self, data=None, message="", status_type="success",
#                         http_status=status.HTTP_200_OK):
#         return Response(
#             {"status": status_type, "message": message, "data": data},
#             status=http_status
#         )


# # -----------------------------
# # 1. AI Symptom Checker
# # -----------------------------
# class AISymptomCheckerView(BaseAIView):
#     serializer_class = SymptomCheckerSerializer

#     @swagger_auto_schema(
#         operation_summary="AI Symptom Checker",
#         request_body=SymptomCheckerSerializer,
#         responses={200: "Symptom analysis result"}
#     )
#     def post(self, request, *args, **kwargs):
#         logger.info(f"Symptom checker called by user {request.user.id}")
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         result = call_gemini(f"Analyze these symptoms: {serializer.validated_data['symptoms']}")

#         return self.format_response(
#             data={"analysis": result},
#             message="Symptom analysis completed."
#         )


# # -----------------------------
# # 2. AI Medical Summary
# # -----------------------------
# class AIMedicalSummaryView(BaseAIView):
#     serializer_class = MedicalSummarySerializer

#     @swagger_auto_schema(
#         operation_summary="AI Medical Summary",
#         request_body=MedicalSummarySerializer,
#         responses={200: "Medical summary result"}
#     )
#     def post(self, request, *args, **kwargs):
#         logger.info(f"Medical summary called by user {request.user.id}")
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         summary = call_gemini(f"Generate a medical summary: {serializer.validated_data['medical_history']}")

#         return self.format_response(
#             data={"summary": summary},
#             message="Medical summary generated."
#         )


# # -----------------------------
# # 3. AI Doctor Recommendation
# # -----------------------------
# class AIDoctorRecommendationView(BaseAIView):
#     serializer_class = DoctorRecommendationSerializer

#     @swagger_auto_schema(
#         operation_summary="AI Doctor Recommendation",
#         request_body=DoctorRecommendationSerializer,
#         responses={200: "Doctor recommendation output"}
#     )
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         symptoms = serializer.validated_data["symptoms"]
#         location = serializer.validated_data["location"]

#         doctors = DoctorProfile.objects.filter(location__icontains=location)

#         if not doctors.exists():
#             return self.format_response(
#                 data=[],
#                 message="No doctors available in this location.",
#                 status_type="error",
#                 http_status=status.HTTP_404_NOT_FOUND
#             )

#         recommendation = call_gemini(
#             f"Recommend doctors for symptoms '{symptoms}' in location '{location}' from list: {[d.user.username for d in doctors]}"
#         )

#         return self.format_response(
#             data={"recommendation": recommendation},
#             message="Doctor recommendation generated."
#         )


# # -----------------------------
# # 4. Admin AI Insights
# # -----------------------------
# class AdminAIInsightsView(APIView):
#     """
#     Generates AI insights for the admin dashboard:
#     - Top doctors by appointments
#     - Appointment trends
#     - High-risk patients (frequent cancellations)
#     """
#     permission_classes = [IsAdminUser]

#     @swagger_auto_schema(
#         operation_summary="AI Admin Insights",
#         request_body=AdminAIInsightsSerializer,
#         responses={200: "AI-generated insights for admin"}
#     )
#     def post(self, request):
#         serializer = AdminAIInsightsSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Get date range from request or defaults
#         end_date = serializer.validated_data.get("end_date", datetime.today().date())
#         start_date = serializer.validated_data.get("start_date", end_date - timedelta(days=30))

#         # 1️⃣ Top doctors by number of appointments
#         top_doctors = (
#             Appointment.objects
#             .filter(date__gte=start_date, date__lte=end_date)
#             .values("doctor__user__username")
#             .annotate(total_appointments=Count("id"))
#             .order_by("-total_appointments")[:5]
#         )

#         # 2️⃣ Appointment trends per day
#         trend_data = (
#             Appointment.objects
#             .filter(date__gte=start_date, date__lte=end_date)
#             .extra({"day": "date(date)"})
#             .values("day")
#             .annotate(total=Count("id"))
#             .order_by("day")
#         )

#         # 3️⃣ High-risk patients by cancellations
#         high_risk_patients = (
#             Appointment.objects
#             .filter(date__gte=start_date, date__lte=end_date, status=Appointment.STATUS_CANCELLED)
#             .values("patient__user__username")
#             .annotate(cancelled_count=Count("id"))
#             .order_by("-cancelled_count")[:5]
#         )

#         # 4️⃣ Generate AI insights using Gemini
#         insight_text = call_gemini(
#             f"Summarize the following appointment trends for admin: {list(trend_data)}"
#         )

#         return Response({
#             "top_doctors": list(top_doctors),
#             "appointment_trend": list(trend_data),
#             "high_risk_patients": list(high_risk_patients),
#             "ai_summary": insight_text
#         })




























































# from rest_framework import generics, permissions, status
# from rest_framework.response import Response 
# from rest_framework.views import APIView
# from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
# from rest_framework.permissions import IsAdminUser 
# from appointments.models import Appointment 
# from users.models import User 
# from django.db.models import Count 
# from datetime import datetime, timedelta 
# from .gemini_utils import call_gemini
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# import logging

# from .serializers import (
#     SymptomCheckerSerializer,
#     MedicalSummarySerializer,
#     DoctorRecommendationSerializer,
# )
# from .gemini_utils import ( 
#     call_gemini,  
# )
# from doctors.models import DoctorProfile  # ✅ Use DoctorProfile instead of Doctor

# logger = logging.getLogger("ai")


# # --------------------------------------------------
# # Base AI View
# # --------------------------------------------------
# class BaseAIView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     throttle_classes = [UserRateThrottle, ScopedRateThrottle]
#     throttle_scope = "ai"
#     http_method_names = ["post"]

#     def format_response(self, data=None, message="", status_type="success",
#                         http_status=status.HTTP_200_OK):
#         return Response(
#             {"status": status_type, "message": message, "data": data},
#             status=http_status
#         )


# # --------------------------------------------------
# # 1. AI Symptom Checker
# # --------------------------------------------------
# class AISymptomCheckerView(BaseAIView):
#     serializer_class = SymptomCheckerSerializer

#     @swagger_auto_schema(
#         operation_summary="AI Symptom Checker",
#         request_body=SymptomCheckerSerializer,
#         responses={200: "Symptom analysis result"}
#     )
#     def post(self, request, *args, **kwargs):
#         logger.info(f"Symptom checker called by user {request.user.id}")
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         result = call_gemini(f"Analyze these symptoms: {serializer.validated_data['symptoms']}")

#         return self.format_response(
#             data={"analysis": result},
#             message="Symptom analysis completed."
#         )


# # --------------------------------------------------
# # 2. AI Medical Summary
# # --------------------------------------------------
# class AIMedicalSummaryView(BaseAIView):
#     serializer_class = MedicalSummarySerializer

#     @swagger_auto_schema(
#         operation_summary="AI Medical Summary",
#         request_body=MedicalSummarySerializer,
#         responses={200: "Medical summary result"}
#     )
#     def post(self, request, *args, **kwargs):
#         logger.info(f"Medical summary called by user {request.user.id}")
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         summary = call_gemini(f"Generate a medical summary: {serializer.validated_data['medical_history']}")

#         return self.format_response(
#             data={"summary": summary},
#             message="Medical summary generated."
#         )


# # --------------------------------------------------
# # 3. AI Doctor Recommendation
# # --------------------------------------------------
# class AIDoctorRecommendationView(BaseAIView):
#     serializer_class = DoctorRecommendationSerializer

#     @swagger_auto_schema(
#         operation_summary="AI Doctor Recommendation",
#         request_body=DoctorRecommendationSerializer,
#         responses={200: "Doctor recommendation output"}
#     )
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         symptoms = serializer.validated_data["symptoms"]
#         location = serializer.validated_data["location"]

#         doctors = DoctorProfile.objects.filter(location__icontains=location)

#         if not doctors.exists():
#             return self.format_response(
#                 data=[],
#                 message="No doctors available in this location.",
#                 status_type="error",
#                 http_status=status.HTTP_404_NOT_FOUND
#             )

#         recommendation = call_gemini(
#             f"Recommend doctors for symptoms '{symptoms}' in location '{location}' from list: {[d.user.username for d in doctors]}"
#         )

#         return self.format_response(
#             data={"recommendation": recommendation},
#             message="Doctor recommendation generated."
#         )


# class AdminAIInsightsView(APIView):
#     """
#     Generates AI insights for admin dashboard:
#     - Top doctors by appointments
#     - Appointment trends
#     - High-risk patients (based on cancellations)
#     """
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         today = datetime.today().date()
#         last_30_days = today - timedelta(days=30)

#         # 1️⃣ Top doctors by number of appointments
#         top_doctors = (
#             Appointment.objects
#             .filter(date__gte=last_30_days)
#             .values("doctor__user__username")
#             .annotate(total_appointments=Count("id"))
#             .order_by("-total_appointments")[:5]
#         )

#     # 2️⃣ Appointment trend over last 30 days
#         trend_data = (
#             Appointment.objects
#             .filter(date__gte=last_30_days)
#             .extra({"day": "date(date)"})
#             .values("day")
#             .annotate(total=Count("id"))
#             .order_by("day")
#         )  
        
#     # 3️⃣ High-risk patients (frequent cancellations)
#         high_risk_patients = (
#             Appointment.objects
#             .filter(date__gte=last_30_days, status=Appointment.STATUS_CANCELLED)
#             .values("patient__user__username")
#             .annotate(cancelled_count=Count("id"))
#             .order_by("-cancelled_count")[:5]
#         ) 
        
#         insight_text = call_gemini(
#             f"Summarize the following appointment trends for admin: {list(trend_data)}"
#         )
        
#         return Response({
#             "top_doctors": list(top_doctors),
#             "appointment_trend": list(trend_data),
#             "high_risk_patients": list(high_risk_patients)
#         }) 











