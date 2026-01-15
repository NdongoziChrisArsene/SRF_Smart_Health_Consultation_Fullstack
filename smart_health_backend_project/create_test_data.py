# backend/create_test_data.py
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_health_backend_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import time, timedelta
from patients.models import PatientProfile
from doctors.models import DoctorProfile, Availability
from appointments.models import Appointment

User = get_user_model()

def create_test_data():
    print("🚀 Creating test data...")
    
    # 1. Create Admin User
    print("\n1️⃣ Creating admin user...")
    admin_user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@test.com",
            "role": "admin",
            "is_staff": True,
            "is_superuser": True,
        }
    )
    if created:
        admin_user.set_password("admin123")
        admin_user.save()
        print(f"✅ Admin created: {admin_user.username}")
    else:
        print(f"ℹ️  Admin already exists: {admin_user.username}")
    
    # 2. Create Test Patient
    print("\n2️⃣ Creating test patient...")
    patient_user, created = User.objects.get_or_create(
        username="patient1",
        defaults={
            "email": "patient1@test.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "patient",
        }
    )
    if created:
        patient_user.set_password("patient123")
        patient_user.save()
        print(f"✅ Patient user created: {patient_user.username}")
    else:
        print(f"ℹ️  Patient user already exists: {patient_user.username}")
    
    # Create patient profile
    patient_profile, created = PatientProfile.objects.get_or_create(
        user=patient_user,
        defaults={
            "date_of_birth": "1990-01-01",
            "phone": "+250788123456",
            "address": "Kigali, Rwanda",
            "medical_history": "No major health issues",
        }
    )
    if created:
        print(f"✅ Patient profile created")
    else:
        print(f"ℹ️  Patient profile already exists")
    
    # 3. Create Test Doctors with Availability
    print("\n3️⃣ Creating test doctors with availability...")
    
    doctors_data = [
        {
            "username": "dr_smith",
            "email": "dr.smith@test.com",
            "first_name": "Robert",
            "last_name": "Smith",
            "specialization": "Cardiology",
            "location": "Kigali",
            "bio": "Experienced cardiologist with 15 years of practice",
            "years_of_experience": 15,
            "phone": "+250788111111",
        },
        {
            "username": "dr_johnson",
            "email": "dr.johnson@test.com",
            "first_name": "Sarah",
            "last_name": "Johnson",
            "specialization": "General Practice",
            "location": "Kigali",
            "bio": "Family medicine specialist",
            "years_of_experience": 10,
            "phone": "+250788222222",
        },
        {
            "username": "dr_williams",
            "email": "dr.williams@test.com",
            "first_name": "Michael",
            "last_name": "Williams",
            "specialization": "Pediatrics",
            "location": "Kigali",
            "bio": "Pediatric specialist focusing on child health",
            "years_of_experience": 8,
            "phone": "+250788333333",
        },
    ]
    
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    for doc_data in doctors_data:
        # Create doctor user
        doctor_user, created = User.objects.get_or_create(
            username=doc_data["username"],
            defaults={
                "email": doc_data["email"],
                "first_name": doc_data["first_name"],
                "last_name": doc_data["last_name"],
                "role": "doctor",
            }
        )
        if created:
            doctor_user.set_password("doctor123")
            doctor_user.save()
            print(f"✅ Doctor user created: {doctor_user.username}")
        else:
            print(f"ℹ️  Doctor user exists: {doctor_user.username}")
        
        # Create doctor profile
        doctor_profile, created = DoctorProfile.objects.get_or_create(
            user=doctor_user,
            defaults={
                "specialization": doc_data["specialization"],
                "location": doc_data["location"],
                "bio": doc_data["bio"],
                "years_of_experience": doc_data["years_of_experience"],
                "phone_number": doc_data["phone"],
                "is_verified": True,
            }
        )
        if created:
            print(f"   ✅ Profile created for Dr. {doc_data['last_name']}")
        else:
            # Update to ensure verified
            doctor_profile.is_verified = True
            doctor_profile.save()
            print(f"   ℹ️  Profile exists for Dr. {doc_data['last_name']}")
        
        # Create availability for weekdays
        availability_count = 0
        for day in weekdays:
            availability, created = Availability.objects.get_or_create(
                doctor=doctor_profile,
                day_of_week=day,
                defaults={
                    "start_time": time(9, 0),   # 9:00 AM
                    "end_time": time(17, 0),    # 5:00 PM
                }
            )
            if created:
                availability_count += 1
        
        if availability_count > 0:
            print(f"   ✅ Created {availability_count} availability slots")
        else:
            print(f"   ℹ️  Availability already exists")
    
    # 4. Create Sample Appointment
    print("\n4️⃣ Creating sample appointment...")
    try:
        # Get first doctor
        first_doctor = DoctorProfile.objects.filter(is_verified=True).first()
        
        if first_doctor and patient_profile:
            # Create appointment for tomorrow
            tomorrow = timezone.now().date() + timedelta(days=1)
            
            appointment, created = Appointment.objects.get_or_create(
                patient=patient_profile,
                doctor=first_doctor,
                date=tomorrow,
                time=time(10, 0),
                defaults={
                    "reason_for_visit": "Regular check-up",
                    "status": "pending",
                }
            )
            
            if created:
                print(f"✅ Sample appointment created for {tomorrow}")
            else:
                print(f"ℹ️  Sample appointment already exists")
    except Exception as e:
        print(f"⚠️  Could not create sample appointment: {e}")
    
    # 5. Print Summary
    print("\n" + "="*60)
    print("📊 TEST DATA SUMMARY")
    print("="*60)
    print("\n🔐 LOGIN CREDENTIALS:")
    print("\nAdmin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nPatient:")
    print("  Username: patient1")
    print("  Password: patient123")
    print("\nDoctors:")
    print("  Username: dr_smith / dr_johnson / dr_williams")
    print("  Password: doctor123")
    
    print("\n📈 DATABASE STATS:")
    print(f"  Total Users: {User.objects.count()}")
    print(f"  Patients: {PatientProfile.objects.count()}")
    print(f"  Doctors: {DoctorProfile.objects.count()}")
    print(f"  Verified Doctors: {DoctorProfile.objects.filter(is_verified=True).count()}")
    print(f"  Availability Slots: {Availability.objects.count()}")
    print(f"  Appointments: {Appointment.objects.count()}")
    
    print("\n✅ Test data creation complete!")
    print("="*60)

if __name__ == "__main__":
    create_test_data()