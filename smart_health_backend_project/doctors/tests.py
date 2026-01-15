from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import time, timedelta
from django.utils import timezone
from doctors.models import DoctorProfile, Availability, Diagnosis, Prescription
from appointments.models import Appointment

User = get_user_model()


from patients.models import PatientProfile


class DoctorProfileTests(APITestCase):
    def setUp(self):
        # Doctor user
        self.user = User.objects.create_user(
            username="doctor1", password="password123", role="doctor"
        )
        # Ensure a DoctorProfile exists
        DoctorProfile.objects.get_or_create(user=self.user)
        self.client.force_authenticate(self.user)

    def test_get_doctor_profile(self):
        response = self.client.get(reverse("doctor-profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "doctor1")

    def test_non_doctor_cannot_access_profile(self):
        patient = User.objects.create_user(username="patient1", password="pass123", role="patient")
        self.client.force_authenticate(patient)
        response = self.client.get(reverse("doctor-profile"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AvailabilityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="doctor2", password="password123", role="doctor"
        )
        DoctorProfile.objects.get_or_create(user=self.user)
        self.client.force_authenticate(self.user)

    def test_create_availability(self):
        payload = {
            "day_of_week": "Monday",
            "start_time": "09:00",
            "end_time": "12:00",
        }
        response = self.client.post(reverse("doctor-availability"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Availability.objects.count(), 1)

    def test_overlapping_availability_fails(self):
        payload1 = {"day_of_week": "Monday", "start_time": "09:00", "end_time": "12:00"}
        payload2 = {"day_of_week": "Monday", "start_time": "11:00", "end_time": "13:00"}
        self.client.post(reverse("doctor-availability"), payload1)
        response = self.client.post(reverse("doctor-availability"), payload2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DiagnosisTests(APITestCase):
    def setUp(self):
        # Create doctor and patient
        self.doctor = User.objects.create_user(username="doctor3", password="pass123", role="doctor")
        self.patient = User.objects.create_user(username="patient2", password="pass123", role="patient")
        # Ensure profiles exist
        self.doctor_profile, _ = DoctorProfile.objects.get_or_create(user=self.doctor)
        self.patient_profile, _ = PatientProfile.objects.get_or_create(user=self.patient)
        self.client.force_authenticate(self.doctor)

        # Create appointment in the near future
        future_date = (timezone.now() + timedelta(days=1)).date().isoformat()
        self.appointment = Appointment.objects.create(
            doctor=self.doctor_profile,
            patient=self.patient_profile,
            date=future_date,
            time="10:00:00"
        )

    def test_doctor_can_create_diagnosis(self):
        payload = {
            "appointment": self.appointment.id,
            "diagnosis": "Flu",
            "notes": "Rest and hydration",
            "prescriptions": [
                {"medicine_name": "Medicine A", "dosage": "1 pill", "duration": "5 days"},
                {"medicine_name": "Medicine B", "dosage": "2 pills", "duration": "3 days"}
            ]
        }
        response = self.client.post(reverse("create-diagnosis"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Diagnosis.objects.count(), 1)
        self.assertEqual(Prescription.objects.count(), 2)

    def test_non_assigned_doctor_cannot_create_diagnosis(self):
        other_doctor = User.objects.create_user(username="doctor4", password="pass123", role="doctor")
        self.client.force_authenticate(other_doctor)

        payload = {
            "appointment": self.appointment.id,
            "diagnosis": "Flu",
            "notes": "Rest",
            "prescriptions": []
        }
        response = self.client.post(reverse("create-diagnosis"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_cannot_create_diagnosis(self):
        self.client.force_authenticate(self.patient)
        payload = {
            "appointment": self.appointment.id,
            "diagnosis": "Flu",
            "notes": "Rest",
            "prescriptions": []
        }
        response = self.client.post(reverse("create-diagnosis"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrescriptionPDFTests(APITestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username="doctor5", password="pass123", role="doctor")
        self.patient = User.objects.create_user(username="patient3", password="pass123", role="patient")
        # Ensure profiles exist
        self.doctor_profile, _ = DoctorProfile.objects.get_or_create(user=self.doctor)
        self.patient_profile, _ = PatientProfile.objects.get_or_create(user=self.patient)
        self.client.force_authenticate(self.doctor)

        future_date = (timezone.now() + timedelta(days=1)).date().isoformat()
        self.appointment = Appointment.objects.create(
            doctor=self.doctor_profile,
            patient=self.patient_profile,
            date=future_date,
            time="11:00:00"
        )

        self.diagnosis = Diagnosis.objects.create(
            appointment=self.appointment,
            diagnosis="Cold",
            notes="Drink fluids"
        )

    def test_doctor_can_download_pdf(self):
        url = reverse("prescription-pdf", args=[self.diagnosis.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_patient_can_download_pdf(self):
        self.client.force_authenticate(self.patient)
        url = reverse("prescription-pdf", args=[self.diagnosis.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_download_pdf(self):
        other_user = User.objects.create_user(username="user1", password="pass123", role="patient")
        self.client.force_authenticate(other_user)
        url = reverse("prescription-pdf", args=[self.diagnosis.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)











