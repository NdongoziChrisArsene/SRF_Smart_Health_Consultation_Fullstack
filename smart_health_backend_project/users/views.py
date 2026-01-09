from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"detail": "User account is disabled"},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )


class AdminUserStatsView(APIView):
    """
    Admin-only user statistics
    period=today|yesterday|last_7_days|last_30_days
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = request.query_params.get("period", "last_7_days")
        today = timezone.now().date()

        ranges = {
            "today": (today, today),
            "yesterday": (today - timedelta(days=1), today - timedelta(days=1)),
            "last_7_days": (today - timedelta(days=6), today),
            "last_30_days": (today - timedelta(days=29), today),
        }

        if period not in ranges:
            return Response({"detail": "Invalid period"}, status=400)

        start, end = ranges[period]

        return Response({
            "new_users": User.objects.filter(date_joined__date__range=(start, end)).count(),
            "active_users": User.objects.filter(last_login__date__range=(start, end)).count(),
            "start_date": start,
            "end_date": end,
        })















































# from django.utils import timezone 
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny, IsAdminUser
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken 
# from rest_framework.views import APIView 
# from datetime import timedelta  
# from django.contrib.auth import get_user_model

# from .models import User
# from .serializers import RegisterSerializer, LoginSerializer

# User = get_user_model()


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]
#     http_method_names = ["post"]


# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = [AllowAny]
#     http_method_names = ["post"]

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = authenticate(
#             request=request,
#             username=serializer.validated_data["username"],
#             password=serializer.validated_data["password"],
#         )


#         if not user:
#             return Response(
#                 {"detail": "Invalid username or password"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         if not user.is_active:
#             return Response(
#                 {"detail": "User account is disabled"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         refresh = RefreshToken.for_user(user)

#         return Response(
#             {
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#                 "username": user.username,
#                 "role": user.role,
#             },
#             status=status.HTTP_200_OK,
#         )

# class AdminUserStatsView(APIView):
#     """
#     Returns counts of new and active users over a specified period.
#     Query param: period=today|yesterday|last_7_days|last_30_days
#     """
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         period = request.query_params.get("period", "last_7_days")
#         today = timezone.now().date()
        
#         if period == "today":
#             start, end = today, today
#         elif period == "yesterday":
#             start, end = today - timedelta(days=1), today - timedelta(days=1)
#         elif period == "last_7_days":
#             start, end = today - timedelta(days=6), today
#         elif period == "last_30_days":
#             start, end = today - timedelta(days=29), today
#         else:
#             return Response({"detail": "Invalid period"}, status=400) 
        
        
#         new_users = User.objects.filter(date_joined__date__range=[start, end]).count()
#         active_users = User.objects.filter(last_login__date__range=[start, end]).count()

#         return Response({
#             "new_users": new_users,
#             "active_users": active_users,
#             "start_date": str(start),
#             "end_date": str(end),
#         })  
