from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]







































# from django.urls import path
# from .views import (
#     RegisterView,
#     LoginView,
#     PasswordResetView,
#     PasswordResetConfirmView,
#     AdminUserStatsView,
# )

# app_name = "users"

# urlpatterns = [
#     path("register/", RegisterView.as_view()),
#     path("login/", LoginView.as_view()),
#     path("password-reset/", PasswordResetView.as_view()),
#     path("password-reset-confirm/", PasswordResetConfirmView.as_view()),
#     path("admin/users/stats/", AdminUserStatsView.as_view()),
# ]






