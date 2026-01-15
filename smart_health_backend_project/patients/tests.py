from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import PatientProfile

User = get_user_model()


class PatientProfileTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="patient1",
            email="patient1@example.com",
            password="securepassword",
            role="patient",
        )

        # Ensure a PatientProfile exists (signals may auto-create it)
        self.profile, _ = PatientProfile.objects.get_or_create(user=self.user)

        # Authenticate the client
        self.client.force_authenticate(user=self.user)

        # URL for profile endpoint (use explicit path to avoid URL reversing quirks in tests)
        self.url = "/api/patients/profile/"

    def test_retrieve_patient_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)

    def test_partial_update_profile(self):
        response = self.client.patch(self.url, {"age": 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = PatientProfile.objects.get(user=self.user)
        self.assertEqual(profile.age, 30)

    def test_full_update_profile(self):
        payload = {
            "age": 35,
            "gender": "female",
            "medical_history": "Diabetic",
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = PatientProfile.objects.get(user=self.user)
        self.assertEqual(profile.age, 35)
        self.assertEqual(profile.gender, "female")
        self.assertEqual(profile.medical_history, "Diabetic")

    def test_profile_not_found(self):
        # Delete the profile
        PatientProfile.objects.filter(user=self.user).delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




























