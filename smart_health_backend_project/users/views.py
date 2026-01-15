from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserSerializer,
)
from .models import User

# Registration
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user.role,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role,
        }, status=status.HTTP_200_OK)

# Password Reset Request
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
            reset_token = RefreshToken.for_user(user).access_token
            reset_link = f"http://localhost:3000/reset-password/{reset_token}"

            send_mail(
                subject="Password Reset Request",
                message=f"Click here to reset your password: {reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except User.DoesNotExist:
            pass  # don't reveal email existence

        return Response(
            {"message": "If the email exists, a reset link has been sent."},
            status=status.HTTP_200_OK,
        )

# Password Reset Confirm
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

# Admin Stats
class AdminUserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
        return Response({
            "total_users": User.objects.count(),
            "patients": User.objects.filter(role="patient").count(),
            "doctors": User.objects.filter(role="doctor").count(),
            "admins": User.objects.filter(role="admin").count(),
        })









































































# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from django.core.mail import send_mail
# from django.conf import settings
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# from .serializers import (
#     RegisterSerializer,
#     LoginSerializer,
#     PasswordResetRequestSerializer,
#     PasswordResetConfirmSerializer,
#     UserSerializer,
# )
# from .models import User


# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)

#             return Response({
#                 "user": UserSerializer(user).data,
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "role": user.role,
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data["user"]
#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "role": user.role,
#         }, status=status.HTTP_200_OK)


# class PasswordResetView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = PasswordResetRequestSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data["email"]

#         try:
#             user = User.objects.get(email=email)

#             reset_token = RefreshToken.for_user(user).access_token
#             reset_link = f"http://localhost:3000/reset-password/{reset_token}"

#             send_mail(
#                 subject="Password Reset Request",
#                 message=f"Click here to reset your password: {reset_link}",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[email],
#                 fail_silently=True,
#             )
#         except User.DoesNotExist:
#             pass  # security: don't reveal email existence

#         return Response(
#             {"message": "If the email exists, a reset link has been sent."},
#             status=status.HTTP_200_OK,
#         )


# class PasswordResetConfirmView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = PasswordResetConfirmSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         token = serializer.validated_data["token"]
#         password = serializer.validated_data["password"]

#         try:
#             access_token = AccessToken(token)
#             user_id = access_token["user_id"]
#             user = User.objects.get(id=user_id)

#             user.set_password(password)
#             user.save()

#             return Response(
#                 {"message": "Password reset successful."},
#                 status=status.HTTP_200_OK,
#             )

#         except Exception:
#             return Response(
#                 {"error": "Invalid or expired token."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


# class AdminUserStatsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         if request.user.role != "admin":
#             return Response(
#                 {"error": "Admin access required"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         return Response({
#             "total_users": User.objects.count(),
#             "patients": User.objects.filter(role="patient").count(),
#             "doctors": User.objects.filter(role="doctor").count(),
#             "admins": User.objects.filter(role="admin").count(),
#         })









