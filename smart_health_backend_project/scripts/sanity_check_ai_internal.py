import os
import sys
from pathlib import Path
import django

# Ensure project root is on PYTHONPATH so settings can be imported
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_health_backend_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

User = get_user_model()

username = 'internal_sanity_user'
password = 'testpassword123'

user, created = User.objects.get_or_create(username=username, defaults={'email': 'internal@example.com'})
if created:
    user.set_password(password)
    user.save()
    print('Created user')
else:
    print('User exists')

refresh = RefreshToken.for_user(user)
access = str(refresh.access_token)

client = APIClient()
client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

resp = client.post('/api/v1/medical/summary/', {'medical_history': 'Patient has cough and fever.'}, format='json', **{'HTTP_HOST': 'testserver'})
print('status:', resp.status_code)
# DRF test client returns a Response-like object; if not, print content
try:
    print('response:', resp.data)
except Exception:
    print('response content:', resp.content)

