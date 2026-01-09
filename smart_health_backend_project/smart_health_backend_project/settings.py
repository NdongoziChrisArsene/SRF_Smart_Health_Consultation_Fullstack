# """
# Django settings for smart_health_backend_project
# Environment-based, PostgreSQL-ready, Render-compatible
# """

# import os
# from pathlib import Path
# from datetime import timedelta

# from dotenv import load_dotenv
# import dj_database_url

# # --------------------------------------------------
# # Base directory
# # --------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

# # --------------------------------------------------
# # Load environment variables
# # --------------------------------------------------
# load_dotenv()  # Render ignores .env and uses dashboard vars

# # --------------------------------------------------
# # Environment
# # --------------------------------------------------
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
# DEBUG = ENVIRONMENT != "production"

# # --------------------------------------------------
# # Secret Key
# # --------------------------------------------------
# SECRET_KEY = os.getenv("SECRET_KEY")

# if not SECRET_KEY:
#     if ENVIRONMENT == "production":
#         raise RuntimeError("SECRET_KEY must be set in production")
#     SECRET_KEY = "dev-secret-key-change-me"

# # --------------------------------------------------
# # Allowed Hosts
# # --------------------------------------------------
# if ENVIRONMENT == "production":
#     ALLOWED_HOSTS = [
#         h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
#     ]
#     if not ALLOWED_HOSTS:
#         raise RuntimeError("ALLOWED_HOSTS must be set in production")
# else:
#     ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# # --------------------------------------------------
# # Installed Apps
# # --------------------------------------------------
# INSTALLED_APPS = [
#     # Django
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # Third-party
#     "rest_framework",
#     "rest_framework.authtoken",
#     "rest_framework_simplejwt.token_blacklist",
#     "corsheaders",

#     # Project apps
#     "users",
#     "patients",
#     "doctors",
#     "appointments",
#     "ai",
#     "notifications",
#     "reports",
# ]

# # --------------------------------------------------
# # Middleware
# # --------------------------------------------------
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "corsheaders.middleware.CorsMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "smart_health_backend_project.urls"
# WSGI_APPLICATION = "smart_health_backend_project.wsgi.application"

# # --------------------------------------------------
# # Templates
# # --------------------------------------------------
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / "templates"],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# # --------------------------------------------------
# # Database (PostgreSQL)
# # --------------------------------------------------
# DATABASE_URL = os.getenv("DATABASE_URL")

# if DATABASE_URL:
#     DATABASES = {
#         "default": dj_database_url.parse(
#             DATABASE_URL,
#             conn_max_age=600,
#             ssl_require=ENVIRONMENT == "production",
#         )
#     }
# else:
#     # LOCAL DEVELOPMENT ONLY
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.getenv("DATABASE_NAME", "smart_health_dev"),
#             "USER": os.getenv("DATABASE_USER", "postgres"),
#             "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
#             "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
#             "PORT": os.getenv("DATABASE_PORT", "5432"),
#         }
#     }

# # --------------------------------------------------
# # Authentication
# # --------------------------------------------------
# AUTH_USER_MODEL = "users.User"

# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# # --------------------------------------------------
# # Django REST Framework
# # --------------------------------------------------
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": (
#         "rest_framework.permissions.IsAuthenticated",
#     ),
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 10,
# }

# # --------------------------------------------------
# # JWT
# # --------------------------------------------------
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
# }

# # --------------------------------------------------
# # CORS & CSRF (Frontend-safe)
# # --------------------------------------------------
# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True
# else:
#     CORS_ALLOW_ALL_ORIGINS = False
#     CORS_ALLOWED_ORIGINS = [
#         o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
#     ]

# CSRF_TRUSTED_ORIGINS = [
#     o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
# ]

# # --------------------------------------------------
# # Security (Production Hardened)
# # --------------------------------------------------
# if ENVIRONMENT == "production":
#     SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_HSTS_SECONDS = 3600
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True

# # --------------------------------------------------
# # Static Files
# # --------------------------------------------------
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"

# # --------------------------------------------------
# # Email (SendGrid / SMTP)
# # --------------------------------------------------
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.sendgrid.net")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "apikey")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
# DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com")

# # --------------------------------------------------
# # Localization
# # --------------------------------------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
# USE_I18N = True
# USE_TZ = True

# # --------------------------------------------------
# # Defaults
# # --------------------------------------------------
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



































































































































"""
Django settings for smart_health_backend_project.
Production-ready, environment-based, conflict-free.
"""

import os
import logging
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv
import dj_database_url

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Base paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# Environment
# --------------------------------------------------
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes") and ENVIRONMENT != "production"

# --------------------------------------------------
# Secret Key
# --------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    if ENVIRONMENT == "production":
        raise RuntimeError("SECRET_KEY must be set in production")
    SECRET_KEY = "dev-secret-key-change-me"

# --------------------------------------------------
# Allowed Hosts
# --------------------------------------------------

ALLOWED_HOSTS = ["*"]

# --------------------------------------------------
# Installed Apps
# --------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_yasg",

    # Project apps
    "users.apps.UsersConfig",
    "patients.apps.PatientsConfig",
    "doctors.apps.DoctorsConfig",
    "appointments.apps.AppointmentsConfig",
    "ai.apps.AiConfig",
    "notifications.apps.NotificationsConfig",
    "reports.apps.ReportsConfig",
]

# --------------------------------------------------
# Middleware
# --------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "smart_health_backend_project.urls"
WSGI_APPLICATION = "smart_health_backend_project.wsgi.application"

# --------------------------------------------------
# Templates
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    if ENVIRONMENT == "production":
        raise RuntimeError("DATABASE_URL must be set in production")

    # Development fallback
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
            "USER": os.getenv("DATABASE_USER", "postgres"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
            "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
            "PORT": os.getenv("DATABASE_PORT", "5432"),
        }
    }


# --------------------------------------------------
# Authentication
# --------------------------------------------------
AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# Django REST Framework
# --------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 10)),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/min",
        "user": "200/min",
    },
}

# --------------------------------------------------
# JWT
# --------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", 60))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("REFRESH_TOKEN_DAYS", 7))),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# --------------------------------------------------
# CORS & CSRF (Frontend Safe)
# --------------------------------------------------
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
    ]

CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

# --------------------------------------------------
# Security
# --------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = ENVIRONMENT == "production"
CSRF_COOKIE_SECURE = ENVIRONMENT == "production"
SECURE_SSL_REDIRECT = ENVIRONMENT == "production"
SECURE_HSTS_SECONDS = 3600 if ENVIRONMENT == "production" else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = ENVIRONMENT == "production"
SECURE_HSTS_PRELOAD = ENVIRONMENT == "production"
SECURE_CONTENT_TYPE_NOSNIFF = ENVIRONMENT == "production"

# --------------------------------------------------
# Static Files
# --------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# --------------------------------------------------
# Email (SMTP)
# --------------------------------------------------
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() in ("1", "true", "yes")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com")

# --------------------------------------------------
# SendGrid (API usage)
# --------------------------------------------------
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_TEMPLATE_APPOINTMENT_BOOKED = os.getenv("SENDGRID_TEMPLATE_APPOINTMENT_BOOKED")
SENDGRID_TEMPLATE_APPOINTMENT_CANCELLED = os.getenv("SENDGRID_TEMPLATE_APPOINTMENT_CANCELLED")
SENDGRID_TEMPLATE_APPOINTMENT_RESCHEDULED = os.getenv("SENDGRID_TEMPLATE_APPOINTMENT_RESCHEDULED")

# --------------------------------------------------
# Logging
# --------------------------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "[{levelname}] {name}: {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "standard"},
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

# --------------------------------------------------
# Localization
# --------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# Defaults
# --------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"






















































































































































# """
# Django settings for smart_health_backend_project.
# Production-ready, environment-based, conflict-free.
# """

# import os
# import logging
# from pathlib import Path
# from datetime import timedelta

# from dotenv import load_dotenv
# import dj_database_url

# # --------------------------------------------------
# # Load environment variables
# # --------------------------------------------------
# load_dotenv()

# # --------------------------------------------------
# # Base paths
# # --------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

# # --------------------------------------------------
# # Environment
# # --------------------------------------------------
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
# DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes") and ENVIRONMENT != "production"

# # --------------------------------------------------
# # Secret Key
# # --------------------------------------------------
# SECRET_KEY = os.getenv("SECRET_KEY")

# if not SECRET_KEY:
#     if ENVIRONMENT == "production":
#         raise RuntimeError("SECRET_KEY must be set in production")
#     SECRET_KEY = "dev-secret-key-change-me"

# # --------------------------------------------------
# # Allowed Hosts
# # --------------------------------------------------
# if ENVIRONMENT == "production":
#     ALLOWED_HOSTS = [
#         h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
#     ]
#     if not ALLOWED_HOSTS:
#         raise RuntimeError("ALLOWED_HOSTS must be set in production")
# else:
#     ALLOWED_HOSTS = ["*"]

# # --------------------------------------------------
# # Installed Apps
# # --------------------------------------------------
# INSTALLED_APPS = [
#     # Django
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # Third-party
#     "rest_framework",
#     "rest_framework.authtoken",
#     "rest_framework_simplejwt.token_blacklist",
#     "corsheaders",
#     "drf_yasg",

#     # Project apps
#     "users.apps.UsersConfig",
#     "patients.apps.PatientsConfig",
#     "doctors.apps.DoctorsConfig",
#     "appointments.apps.AppointmentsConfig",
#     "ai.apps.AiConfig",
#     "notifications.apps.NotificationsConfig",
#     "reports.apps.ReportsConfig",
# ]

# # --------------------------------------------------
# # Middleware
# # --------------------------------------------------
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "corsheaders.middleware.CorsMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "smart_health_backend_project.urls"
# WSGI_APPLICATION = "smart_health_backend_project.wsgi.application"

# # --------------------------------------------------
# # Templates
# # --------------------------------------------------
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / "templates"],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# DATABASE_URL = os.getenv("DATABASE_URL")

# if DATABASE_URL:
#     DATABASES = {
#         "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
#     }
# else:
#     if ENVIRONMENT == "production":
#         raise RuntimeError("DATABASE_URL must be set in production")

#     # Development fallback
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.getenv("DATABASE_NAME", "smart_health_db"),
#             "USER": os.getenv("DATABASE_USER", "postgres"),
#             "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
#             "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
#             "PORT": os.getenv("DATABASE_PORT", "5432"),
#         }
#     }


# # --------------------------------------------------
# # Authentication
# # --------------------------------------------------
# AUTH_USER_MODEL = "users.User"

# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# # --------------------------------------------------
# # Django REST Framework
# # --------------------------------------------------
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": (
#         "rest_framework.permissions.IsAuthenticated",
#     ),
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 10)),
#     "DEFAULT_THROTTLE_CLASSES": (
#         "rest_framework.throttling.AnonRateThrottle",
#         "rest_framework.throttling.UserRateThrottle",
#     ),
#     "DEFAULT_THROTTLE_RATES": {
#         "anon": "20/min",
#         "user": "200/min",
#     },
# }

# # --------------------------------------------------
# # JWT
# # --------------------------------------------------
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", 60))),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("REFRESH_TOKEN_DAYS", 7))),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
# }

# # --------------------------------------------------
# # CORS & CSRF (Frontend Safe)
# # --------------------------------------------------
# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True
# else:
#     CORS_ALLOW_ALL_ORIGINS = False
#     CORS_ALLOWED_ORIGINS = [
#         o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
#     ]

# CSRF_TRUSTED_ORIGINS = [
#     o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
# ]

# # --------------------------------------------------
# # Security
# # --------------------------------------------------
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SESSION_COOKIE_SECURE = ENVIRONMENT == "production"
# CSRF_COOKIE_SECURE = ENVIRONMENT == "production"
# SECURE_SSL_REDIRECT = ENVIRONMENT == "production"
# SECURE_HSTS_SECONDS = 3600 if ENVIRONMENT == "production" else 0
# SECURE_HSTS_INCLUDE_SUBDOMAINS = ENVIRONMENT == "production"
# SECURE_HSTS_PRELOAD = ENVIRONMENT == "production"
# SECURE_CONTENT_TYPE_NOSNIFF = ENVIRONMENT == "production"

# # --------------------------------------------------
# # Static Files
# # --------------------------------------------------
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"

# # --------------------------------------------------
# # Email (SMTP)
# # --------------------------------------------------
# EMAIL_BACKEND = os.getenv(
#     "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
# )
# EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
# EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() in ("1", "true", "yes")
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
# DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com")

# # --------------------------------------------------
# # SendGrid (API usage)
# # --------------------------------------------------
# SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
# SENDGRID_TEMPLATE_APPOINTMENT_BOOKED = os.getenv("SENDGRID_TEMPLATE_APPOINTMENT_BOOKED")
# SENDGRID_TEMPLATE_APPOINTMENT_CANCELLED = os.getenv("SENDGRID_TEMPLATE_APPOINTMENT_CANCELLED")
# SENDGRID_TEMPLATE_APPOINTMENT_RESCHEDULED = os.getenv("SENDGRID_TEMPLATE_APPOINTMENT_RESCHEDULED")

# # --------------------------------------------------
# # Logging
# # --------------------------------------------------
# LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "standard": {"format": "[{levelname}] {name}: {message}", "style": "{"},
#     },
#     "handlers": {
#         "console": {"class": "logging.StreamHandler", "formatter": "standard"},
#     },
#     "root": {"handlers": ["console"], "level": LOG_LEVEL},
# }

# # --------------------------------------------------
# # Localization
# # --------------------------------------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
# USE_I18N = True
# USE_TZ = True

# # --------------------------------------------------
# # Defaults
# # --------------------------------------------------
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"















































