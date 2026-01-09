from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "report_type",
            "date_from",
            "date_to",
            "is_ready",
            "created_at",
        ]
        read_only_fields = ["id", "is_ready", "created_at"]














































# from rest_framework import serializers
# from .models import Report


# class ReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Report 
#         exclude = ("generated_by",)

        # fields = "__all__"
        # read_only_fields = ("generated_by", "created_at", "file", "is_ready")
















# from rest_framework import serializers
# from .models import Report

# class ReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Report
#         fields = "__all__"
#         read_only_fields = ("generated_by", "created_at", "file")














