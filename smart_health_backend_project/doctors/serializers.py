from rest_framework import serializers
from .models import DoctorProfile, Availability, Diagnosis, Prescription

class DoctorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "username",
            "email",
            "specialization",
            "location",
            "years_of_experience",
        ]

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ["id", "day_of_week", "start_time", "end_time"]

    def validate(self, data):
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError("Start time must be before end time.")
        return data

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["medicine_name", "dosage", "duration"]


class DiagnosisSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, required=False)

    class Meta:
        model = Diagnosis
        fields = ["id", "appointment", "diagnosis", "notes", "prescriptions"]

    def create(self, validated_data):
        prescriptions_data = validated_data.pop("prescriptions", [])
        diagnosis = Diagnosis.objects.create(**validated_data)

        for pres in prescriptions_data:
            Prescription.objects.create(diagnosis=diagnosis, **pres)

        return diagnosis







































# from rest_framework import serializers
# from .models import DoctorProfile, Availability, Diagnosis, Prescription


# class DoctorSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="user.username", read_only=True)
#     email = serializers.CharField(source="user.email", read_only=True)

#     class Meta:
#         model = DoctorProfile
#         fields = [
#             "id",
#             "username",
#             "email",
#             "specialization",
#             "location",
#             "years_of_experience",
#         ]
#         read_only_fields = ("id", "username", "email")


# class AvailabilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Availability
#         fields = ["id", "day_of_week", "start_time", "end_time"]

#     def validate(self, data):
#         if data["start_time"] >= data["end_time"]:
#             raise serializers.ValidationError("Start time must be before end time.")
#         return data


# class PrescriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prescription
#         fields = "__all__"


# class DiagnosisSerializer(serializers.ModelSerializer):
#     prescriptions = PrescriptionSerializer(many=True)

#     class Meta:
#         model = Diagnosis
#         fields = ["id", "appointment", "diagnosis", "notes", "prescriptions"]

#     def create(self, validated_data):
#         prescriptions_data = validated_data.pop("prescriptions", [])
#         diagnosis = Diagnosis.objects.create(**validated_data)

#         for pres in prescriptions_data:
#             Prescription.objects.create(diagnosis=diagnosis, **pres)

#         return diagnosis

#     def update(self, instance, validated_data):
#         prescriptions_data = validated_data.pop("prescriptions", [])
#         instance.diagnosis = validated_data.get("diagnosis", instance.diagnosis)
#         instance.notes = validated_data.get("notes", instance.notes)
#         instance.save()

#         if prescriptions_data:
#             instance.prescriptions.all().delete()
#             for pres in prescriptions_data:
#                 Prescription.objects.create(diagnosis=instance, **pres)

#         return instance













































# from rest_framework import serializers
# from .models import DoctorProfile, Availability 
# from .models import Diagnosis, Prescription


# class DoctorSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="user.username", read_only=True)
#     email = serializers.CharField(source="user.email", read_only=True)

#     class Meta:
#         model = DoctorProfile
#         fields = [
#             "id",
#             "username",
#             "email",
#             "specialization",
#             "location",
#             "years_of_experience",
#         ]
#         read_only_fields = ("id", "username", "email")


# class AvailabilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Availability
#         fields = ["id", "day_of_week", "start_time", "end_time"]
#         read_only_fields = ["id"]

#     def validate(self, data):
#         doctor = self.context.get("doctor")
#         if not doctor:
#             raise serializers.ValidationError("Doctor profile is required.")
#         return data


# class PrescriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prescription
#         fields = "__all__"


# class DiagnosisSerializer(serializers.ModelSerializer):
#     prescriptions = PrescriptionSerializer(many=True)

#     class Meta:
#         model = Diagnosis
#         fields = ["id", "appointment", "diagnosis", "notes", "prescriptions"]

#     def create(self, validated_data):
#         prescriptions_data = validated_data.pop("prescriptions")
#         diagnosis = Diagnosis.objects.create(**validated_data)

#         for pres in prescriptions_data:
#             Prescription.objects.create(diagnosis=diagnosis, **pres)

#         return diagnosis








































# from rest_framework import serializers
# from .models import Doctor, Availability


# class DoctorSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="user.username", read_only=True)
#     email = serializers.CharField(source="user.email", read_only=True)

#     class Meta:
#         model = Doctor
#         fields = [
#             "id", "username", "email",
#             "specialization", "location", "years_of_experience"
#         ]
#         read_only_fields = ["id", "username", "email"]


# class AvailabilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Availability
#         fields = ["id", "day_of_week", "start_time", "end_time"]
#         read_only_fields = ["id"]

#     def validate(self, data):
#         doctor = self.context.get("doctor")
#         if not doctor:
#             raise serializers.ValidationError("Doctor profile is required.")
#         return data

