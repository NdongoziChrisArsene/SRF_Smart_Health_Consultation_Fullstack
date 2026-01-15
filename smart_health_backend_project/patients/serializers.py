from rest_framework import serializers
from .models import PatientProfile


class PatientProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = PatientProfile
        fields = [
            'id',
            'username',
            'email', 
            'first_name',
            'last_name',
            'date_of_birth',
            'phone',
            'address',
            'medical_history',
            'emergency_contact',
            'blood_group',
            'allergies',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'date_of_birth': {'required': False},
            'phone': {'required': False},
            'address': {'required': False},
            'medical_history': {'required': False},
            'emergency_contact': {'required': False},
            'blood_group': {'required': False},
            'allergies': {'required': False},
        }


class UpdatePatientSerializer(serializers.ModelSerializer):
    medical_history = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False,
    )
    gender = serializers.ChoiceField(
        choices=PatientProfile.GENDER_CHOICES,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = PatientProfile
        fields = ("age", "gender", "medical_history")























