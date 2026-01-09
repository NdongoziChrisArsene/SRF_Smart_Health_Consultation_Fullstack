from rest_framework import serializers
from datetime import date

# -----------------------------
# 1. Symptom Checker
# -----------------------------
class SymptomCheckerSerializer(serializers.Serializer):
    symptoms = serializers.CharField(
        max_length=1000,
        help_text="Describe the symptoms (comma-separated or plain text)."
    )
    symptoms.swagger_example = "fever, cough, chest pain"

    def validate_symptoms(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Symptoms cannot be empty.")
        return value


# -----------------------------
# 2. Medical Summary
# -----------------------------
class MedicalSummarySerializer(serializers.Serializer):
    medical_history = serializers.CharField(
        max_length=5000,
        help_text="Full medical history text."
    )
    medical_history.swagger_example = "Patient has hypertension and is on medication. Previous surgery in 2018."

    def validate_medical_history(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Medical history cannot be empty.")
        return value


# -----------------------------
# 3. Doctor Recommendation
# -----------------------------
class DoctorRecommendationSerializer(serializers.Serializer):
    symptoms = serializers.CharField(
        max_length=1000,
        help_text="Symptoms to analyze for recommendation."
    )
    location = serializers.CharField(
        max_length=200,
        help_text="City, district or region."
    )
    symptoms.swagger_example = "shortness of breath, chest pain"
    location.swagger_example = "Kigali"

    def validate_symptoms(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Symptoms cannot be empty.")
        return value

    def validate_location(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Location cannot be empty.")
        return value


# -----------------------------
# 4. Admin AI Insights
# -----------------------------
class AdminAIInsightsSerializer(serializers.Serializer):
    start_date = serializers.DateField(
        required=False,
        help_text="Start date for trend analysis (YYYY-MM-DD). Defaults to 30 days ago."
    )
    end_date = serializers.DateField(
        required=False,
        help_text="End date for trend analysis (YYYY-MM-DD). Defaults to today."
    )

    def validate(self, data):
        start = data.get("start_date")
        end = data.get("end_date")
        if start and end and start > end:
            raise serializers.ValidationError("start_date cannot be after end_date.")
        return data


    class Meta:
        swagger_schema_fields = {
            "example": {
                "start_date": "2026-01-01",
                "end_date": "2026-01-31"
            }
        }















































# from rest_framework import serializers

# # 1. Symptom Checker
# class SymptomCheckerSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(max_length=1000, help_text="Describe the symptoms (comma-separated or plain text).")
#     symptoms.swagger_example = "fever, cough, chest pain"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value


# # 2. Medical Summary
# class MedicalSummarySerializer(serializers.Serializer):
#     medical_history = serializers.CharField(max_length=5000, help_text="Full medical history text.")
#     medical_history.swagger_example = "Patient has hypertension and is on medication. Previous surgery in 2018."

#     def validate_medical_history(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Medical history cannot be empty.")
#         return value


# # 3. Doctor Recommendation
# class DoctorRecommendationSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(max_length=1000, help_text="Symptoms to analyze for recommendation.")
#     location = serializers.CharField(max_length=200, help_text="City, district or region.")
#     symptoms.swagger_example = "shortness of breath, chest pain"
#     location.swagger_example = "Kigali"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value

#     def validate_location(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Location cannot be empty.")
#         return value





















































# from rest_framework import serializers

# # 1. Symptom Checker
# class SymptomCheckerSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(max_length=1000, help_text="Describe the symptoms (comma-separated or plain text).")
#     symptoms.swagger_example = "fever, cough, chest pain"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value


# # 2. Medical Summary
# class MedicalSummarySerializer(serializers.Serializer):
#     medical_history = serializers.CharField(max_length=5000, help_text="Full medical history text.")
#     medical_history.swagger_example = "Patient has hypertension and is on medication. Previous surgery in 2018."

#     def validate_medical_history(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Medical history cannot be empty.")
#         return value


# # 3. Doctor Recommendation
# class DoctorRecommendationSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(max_length=1000, help_text="Symptoms to analyze for recommendation.")
#     location = serializers.CharField(max_length=200, help_text="City, district or region.")
#     symptoms.swagger_example = "shortness of breath, chest pain"
#     location.swagger_example = "Kigali"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value

#     def validate_location(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Location cannot be empty.")
#         return value























































# from rest_framework import serializers


# # =====================================================
# # 1. Symptom Checker
# # =====================================================
# class SymptomCheckerSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(
#         max_length=1000,
#         help_text="Describe the symptoms (comma-separated or plain text).",
#     )

#     symptoms.swagger_example = "fever, cough, chest pain"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value


# # =====================================================
# # 2. Medical Summary
# # =====================================================
# class MedicalSummarySerializer(serializers.Serializer):
#     medical_history = serializers.CharField(
#         max_length=5000,
#         help_text="Full medical history text.",
#     )

#     medical_history.swagger_example = (
#         "Patient has hypertension and is on medication. Previous surgery in 2018."
#     )

#     def validate_medical_history(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Medical history cannot be empty.")
#         return value


# # =====================================================
# # 3. Doctor Recommendation
# # =====================================================
# class DoctorRecommendationSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(
#         max_length=1000,
#         help_text="Symptoms to analyze for recommendation.",
#     )
#     location = serializers.CharField(
#         max_length=200,
#         help_text="City, district or region.",
#     )

#     symptoms.swagger_example = "shortness of breath, chest pain"
#     location.swagger_example = "Kigali"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value

#     def validate_location(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Location cannot be empty.")
#         return value
