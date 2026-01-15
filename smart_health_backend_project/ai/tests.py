from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from doctors.models import DoctorProfile

User = get_user_model()


class AITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password", email="test@example.com")
        self.client.force_authenticate(user=self.user)

    @patch("ai.views.call_gemini")
    def test_medical_summary_returns_summary(self, mock_call):
        mock_call.return_value = "This is a mocked medical summary."
        url = "/api/v1/medical/summary/"
        payload = {"medical_history": "Patient has fever and cough."}

        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("summary", data["data"])
        self.assertEqual(data["data"]["summary"], "This is a mocked medical summary.")

    @patch("ai.views.call_gemini")
    def test_symptom_checker_returns_analysis(self, mock_call):
        mock_call.return_value = "Mocked analysis"
        url = "/api/v1/symptoms/checker/"
        payload = {"symptoms": "headache and nausea"}

        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("analysis", data["data"])
        self.assertEqual(data["data"]["analysis"], "Mocked analysis")

    @patch("ai.views.call_gemini")
    def test_doctor_recommendation_returns_recommendation_when_doctors_exist(self, mock_call):
        mock_call.return_value = "Recommended Doctor A"
        # create a doctor user and profile
        doc_user = User.objects.create_user(username="doc1", password="password", email="doc1@example.com", role=User.ROLE_DOCTOR)
        DoctorProfile.objects.update_or_create(user=doc_user, defaults={"specialization":"General","location":"TestCity","years_of_experience":5,"is_verified":True})

        url = "/api/v1/doctors/recommendation/"
        payload = {"symptoms": "sore throat", "location": "TestCity"}

        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("recommendation", data["data"])
        self.assertEqual(data["data"]["recommendation"], "Recommended Doctor A")

    def test_doctor_recommendation_no_doctors_returns_404(self):
        url = "/api/v1/doctors/recommendation/"
        payload = {"symptoms": "sore throat", "location": "NowhereTown"}

        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        data = resp.json()
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["data"], [])

