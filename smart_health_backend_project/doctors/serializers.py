from rest_framework import serializers
from .models import DoctorProfile, Availability, Diagnosis, Prescription


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'day_of_week', 'start_time', 'end_time']


class DoctorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    availability = AvailabilitySerializer(many=True, read_only=True)
    
    class Meta:
        model = DoctorProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'specialization',
            'location',
            'bio',
            'years_of_experience',
            'phone_number',
            'is_verified',
            'rating',
            'availability',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'is_verified', 'rating', 'created_at', 'updated_at']


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["id", "medicine_name", "dosage", "duration"]


class DiagnosisSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, required=False)
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    appointment_date = serializers.DateField(source='appointment.date', read_only=True)
    appointment_time = serializers.TimeField(source='appointment.time', read_only=True)

    class Meta:
        model = Diagnosis
        fields = [
            "id", 
            "appointment", 
            "diagnosis", 
            "notes", 
            "prescriptions",
            "patient_name",
            "doctor_name",
            "appointment_date",
            "appointment_time",
            "created_at"
        ]
        read_only_fields = ['id', 'created_at', 'patient_name', 'doctor_name']

    def get_patient_name(self, obj):
        """Get patient name from appointment"""
        patient = obj.appointment.patient
        user = getattr(patient, 'user', patient)
        return user.get_full_name() or user.username

    def get_doctor_name(self, obj):
        """Get doctor name from appointment"""
        doctor = obj.appointment.doctor
        user = getattr(doctor, 'user', doctor)
        return user.get_full_name() or user.username

    def create(self, validated_data):
        prescriptions_data = validated_data.pop("prescriptions", [])
        diagnosis = Diagnosis.objects.create(**validated_data)

        for pres in prescriptions_data:
            Prescription.objects.create(diagnosis=diagnosis, **pres)

        return diagnosis









