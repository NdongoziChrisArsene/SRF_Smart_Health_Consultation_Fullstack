# smart_health_backend_project/celery.py

import os
from celery import Celery
from dotenv import load_dotenv
from pathlib import Path

# --------------------------------------------------
# Load .env
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# Django settings
# --------------------------------------------------
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "smart_health_backend_project.settings",
)

# --------------------------------------------------
# Celery app
# --------------------------------------------------
app = Celery("smart_health_backend_project")

# Load settings with CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all apps
app.autodiscover_tasks()
