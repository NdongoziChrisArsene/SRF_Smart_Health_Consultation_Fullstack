import requests
import os

BASE = os.getenv('BASE_URL', 'http://127.0.0.1:8000')
register_url = f"{BASE}/api/auth/register/"
login_url = f"{BASE}/api/auth/login/"
summary_url = f"{BASE}/api/v1/medical/summary/"

session = requests.Session()

print('Creating test user...')
resp = session.post(register_url, json={
    'username': 'sanity_test_user',
    'password': 'testpassword123',
    'email': 'sanity@example.com'
})
print('register status:', resp.status_code, resp.text)

print('Logging in...')
resp = session.post(login_url, json={'username': 'sanity_test_user', 'password': 'testpassword123'})
print('login status:', resp.status_code, resp.text)
if resp.status_code != 200:
    raise SystemExit('Login failed')

access = resp.json().get('access')
headers = {'Authorization': f'Bearer {access}'}

print('Calling medical summary endpoint...')
resp = session.post(summary_url, json={'medical_history': 'Patient has cough and fever.'}, headers=headers)
print('summary status:', resp.status_code)
print('response:', resp.text)
