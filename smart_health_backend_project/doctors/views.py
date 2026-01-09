from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas

from .models import DoctorProfile, Availability, Diagnosis
from .serializers import DoctorSerializer, AvailabilitySerializer, DiagnosisSerializer
from users.permissions import IsDoctor, IsPatient

class DoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_object(self):
        doctor = getattr(self.request.user, "doctor_profile", None)
        if not doctor:
            raise NotFound("Doctor profile not found")
        return doctor
    
class AvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Availability.objects.filter(doctor=self.request.user.doctor_profile)

    def perform_create(self, serializer):
        instance = serializer.save(doctor=self.request.user.doctor_profile)
        instance.full_clean()
        instance.save()

class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Availability.objects.filter(doctor=self.request.user.doctor_profile)

class CreateDiagnosisAPIView(generics.CreateAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        appointment = serializer.validated_data["appointment"]

        if appointment.doctor != self.request.user:
            raise PermissionDenied("You are not assigned to this appointment.")

        serializer.save()

class DoctorDiagnosisHistoryView(generics.ListAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Diagnosis.objects.filter(
            appointment__doctor=self.request.user
        )

class PatientDiagnosisHistoryView(generics.ListAPIView):
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_queryset(self):
        return Diagnosis.objects.filter(
            appointment__patient=self.request.user
        )

class PrescriptionPDFView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, diagnosis_id):
        diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)

        if (
            diagnosis.appointment.doctor != request.user
            and diagnosis.appointment.patient != request.user
        ):
            raise PermissionDenied("Not allowed")

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="prescription.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 800, "Medical Prescription")
        p.drawString(100, 770, f"Diagnosis: {diagnosis.diagnosis}")
        p.drawString(100, 740, f"Notes: {diagnosis.notes}")

        y = 700
        for pres in diagnosis.prescriptions.all():
            p.drawString(
                100, y,
                f"{pres.medicine_name} - {pres.dosage} - {pres.duration}"
            )
            y -= 20

        p.showPage()
        p.save()
        return response


















































# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound, PermissionDenied
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
# from reportlab.pdfgen import canvas

# from .models import DoctorProfile, Availability, Diagnosis
# from .serializers import DoctorSerializer, AvailabilitySerializer, DiagnosisSerializer
# from users.permissions import IsDoctor, IsPatient
# from appointments.models import Appointment

# class DoctorProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = DoctorSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_object(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")
#         return doctor

# class AvailabilityListCreateView(generics.ListCreateAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         return Availability.objects.filter(doctor=self.request.user.doctor_profile)

#     def perform_create(self, serializer):
#         serializer.save(doctor=self.request.user.doctor_profile)

# class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         return Availability.objects.filter(doctor=self.request.user.doctor_profile)

# class CreateDiagnosisAPIView(generics.CreateAPIView):
#     serializer_class = DiagnosisSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def perform_create(self, serializer):
#         appointment = serializer.validated_data["appointment"]

#         if appointment.doctor != self.request.user:
#             raise PermissionDenied("You are not assigned to this appointment.")

#         serializer.save()

# class DoctorDiagnosisHistoryView(generics.ListAPIView):
#     serializer_class = DiagnosisSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         return Diagnosis.objects.filter(
#             appointment__doctor=self.request.user
#         )

# class PatientDiagnosisHistoryView(generics.ListAPIView):
#     serializer_class = DiagnosisSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPatient]

#     def get_queryset(self):
#         return Diagnosis.objects.filter(
#             appointment__patient=self.request.user
#         )

# class PrescriptionPDFView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, diagnosis_id):
#         diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)

#         if (
#             diagnosis.appointment.doctor != request.user
#             and diagnosis.appointment.patient != request.user
#         ):
#             raise PermissionDenied("Not allowed")

#         response = HttpResponse(content_type="application/pdf")
#         response["Content-Disposition"] = 'attachment; filename="prescription.pdf"'

#         p = canvas.Canvas(response)
#         p.drawString(100, 800, "Medical Prescription")
#         p.drawString(100, 770, f"Diagnosis: {diagnosis.diagnosis}")
#         p.drawString(100, 740, f"Notes: {diagnosis.notes}")

#         y = 700
#         for pres in diagnosis.prescriptions.all():
#             p.drawString(
#                 100, y,
#                 f"{pres.medicine_name} - {pres.dosage} - {pres.duration}"
#             )
#             y -= 20

#         p.showPage()
#         p.save()
#         return response

























































# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound, PermissionDenied
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
# from reportlab.pdfgen import canvas

# from .models import DoctorProfile, Availability, Diagnosis
# from .serializers import DoctorSerializer, AvailabilitySerializer, DiagnosisSerializer
# from users.permissions import IsDoctor


# class DoctorProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = DoctorSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_object(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")
#         return doctor


# class AvailabilityListCreateView(generics.ListCreateAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")
#         return Availability.objects.filter(doctor=doctor)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["doctor"] = getattr(self.request.user, "doctor_profile", None)
#         return context

#     def perform_create(self, serializer):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         instance = serializer.save(doctor=doctor)
#         instance.full_clean()
#         instance.save()


# class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")
#         return Availability.objects.filter(doctor=doctor)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["doctor"] = getattr(self.request.user, "doctor_profile", None)
#         return context


# class CreateDiagnosisAPIView(generics.CreateAPIView):
#     queryset = Diagnosis.objects.all()
#     serializer_class = DiagnosisSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def perform_create(self, serializer):
#         appointment = serializer.validated_data["appointment"]
#         doctor_profile = getattr(self.request.user, "doctor_profile", None)

#         if not doctor_profile:
#             raise PermissionDenied("Doctor profile not found.")

#         if appointment.doctor != self.request.user:
#             raise PermissionDenied("You are not assigned to this appointment.")

#         serializer.save()


# class DoctorDiagnosisHistoryView(generics.ListAPIView):
#     serializer_class = DiagnosisSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         return Diagnosis.objects.filter(
#             appointment__doctor=self.request.user
#         ).select_related("appointment")


# class PatientDiagnosisHistoryView(generics.ListAPIView):
#     serializer_class = DiagnosisSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Diagnosis.objects.filter(
#             appointment__patient=self.request.user
#         ).select_related("appointment")


# class PrescriptionPDFView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, diagnosis_id):
#         diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)

#         # Authorization: doctor OR patient
#         if (
#             diagnosis.appointment.doctor != request.user
#             and diagnosis.appointment.patient != request.user
#         ):
#             raise PermissionDenied("Not allowed to view this prescription")

#         response = HttpResponse(content_type="application/pdf")
#         response["Content-Disposition"] = 'attachment; filename="prescription.pdf"'

#         p = canvas.Canvas(response)
#         p.drawString(100, 800, "Medical Prescription")
#         p.drawString(100, 770, f"Diagnosis: {diagnosis.diagnosis}")
#         p.drawString(100, 740, f"Notes: {diagnosis.notes}")

#         y = 700
#         for pres in diagnosis.prescriptions.all():
#             p.drawString(
#                 100,
#                 y,
#                 f"{pres.medicine_name} - {pres.dosage} - {pres.duration}",
#             )
#             y -= 20

#         p.showPage()
#         p.save()
#         return response























































# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound
# from .models import DoctorProfile, Availability, Diagnosis, Appointment
# from .serializers import DoctorSerializer, AvailabilitySerializer, DiagnosisSerializer 
# from users.permissions import IsDoctor
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from django.shortcuts import get_object_or_404


# class DoctorProfileView(generics.RetrieveUpdateAPIView):
#     """
#     Retrieve & update the authenticated doctor's profile.
#     """
#     serializer_class = DoctorSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_object(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")
#         return doctor


# class AvailabilityListCreateView(generics.ListCreateAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")
#         return Availability.objects.filter(doctor=doctor)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["doctor"] = getattr(self.request.user, "doctor_profile", None)
#         return context

#     def perform_create(self, serializer):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         instance = serializer.save(doctor=doctor)
#         instance.full_clean()
#         instance.save()


# class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")
#         return Availability.objects.filter(doctor=doctor)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["doctor"] = getattr(self.request.user, "doctor_profile", None)
#         return context

# class CreateDiagnosisAPIView(generics.CreateAPIView): 
#     queryset = Diagnosis.objects.all()
#     serializer_class = DiagnosisSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def perform_create(self, serializer):  
#         appointment = serializer.validated_data["appointment"]
#         doctor_profile = getattr(self.request.user, "doctor_profile", None)  
        
#         if not doctor_profile:
#             raise PermissionDenied("Doctor profile not found.") 
        
#         # Appointment.doctor is User, not DoctorProfile
#         if appointment.doctor != self.request.user:
#             raise PermissionDenied("You are not assigned to this appointment.")

#         serializer.save()         


# class DoctorDiagnosisHistoryView(generics.ListAPIView):
#     serializer_class = DiagnosisSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         return Diagnosis.objects.filter(
#             appointment__doctor=self.request.user
#         ).select_related("appointment")


# class PatientDiagnosisHistoryView(generics.ListAPIView):
#     serializer_class = DiagnosisSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Diagnosis.objects.filter(
#             appointment__patient=self.request.user
#         ).select_related("appointment")


# class PrescriptionPDFView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]  
    
#     def get(self, request, diagnosis_id):
#         diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id) 
        
#     # Authorization
#         if (
#             diagnosis.appointment.doctor != request.user
#             and diagnosis.appointment.patient != request.user
#         ):
#             raise PermissionDenied("Not allowed to view this prescription")

#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = 'attachment; filename="prescription.pdf"'

#     p = canvas.Canvas(response)
#     p.drawString(100, 800, "Medical Prescription")
#     p.drawString(100, 770, f"Diagnosis: {diagnosis.diagnosis}")
#     p.drawString(100, 740, f"Notes: {diagnosis.notes}")

#     y = 700
#     for pres in diagnosis.prescriptions.all():
#         p.drawString(
#             100, y,
#             f"{pres.medicine_name} - {pres.dosage} - {pres.duration}"
#         )
#         y -= 20

#     p.showPage()
#     p.save()
#     return response
























# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound
# from .models import DoctorProfile, Availability
# from .serializers import DoctorSerializer, AvailabilitySerializer
# from users.permissions import IsDoctor


# class DoctorProfileView(generics.RetrieveUpdateAPIView):
#     """
#     GET: Retrieve doctor profile
#     PATCH: Update doctor profile
#     """
#     serializer_class = DoctorSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_object(self):
#         try:
#             return Doctor.objects.get(user=self.request.user)
#         except Doctor.DoesNotExist:
#             raise NotFound("Doctor profile not found")

#     def get_doctor(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")
#         return doctor



# class AvailabilityListCreateView(generics.ListCreateAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")

#         return Availability.objects.filter(doctor=doctor)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["doctor"] = getattr(self.request.user, "doctor_profile", None)
#         return context

#     def perform_create(self, serializer):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         instance = serializer.save(doctor=doctor)
#         instance.full_clean()
#         instance.save()


# class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")

#         return Availability.objects.filter(doctor=doctor)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["doctor"] = getattr(self.request.user, "doctor_profile", None)
#         return context
