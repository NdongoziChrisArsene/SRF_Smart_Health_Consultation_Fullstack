from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

# Registration
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "role", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data["user"] = user
        return data

# Password Reset
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role", "first_name", "last_name"]






































































# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError as DjangoValidationError
# from .models import User


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     password_confirm = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "email",
#             "password",
#             "password_confirm",
#             "first_name",
#             "last_name",
#             "role",
#             "specialization",
#         )

#     def validate(self, attrs):
#         if attrs["password"] != attrs["password_confirm"]:
#             raise serializers.ValidationError("Passwords do not match")

#         try:
#             validate_password(attrs["password"])
#         except DjangoValidationError as e:
#             raise serializers.ValidationError(e.messages)

#         return attrs

#     def create(self, validated_data):
#         validated_data.pop("password_confirm")
#         password = validated_data.pop("password")

#         user = User.objects.create_user(
#             password=password,
#             **validated_data
#         )
#         return user


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(
#             email=data["email"],
#             password=data["password"]
#         )
#         if not user:
#             raise serializers.ValidationError("Invalid credentials")
#         data["user"] = user
#         return data


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "username",
#             "email",
#             "first_name",
#             "last_name",
#             "role",
#             "specialization",
#         )


# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()


# class PasswordResetConfirmSerializer(serializers.Serializer):
#     token = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     password_confirm = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         if attrs["password"] != attrs["password_confirm"]:
#             raise serializers.ValidationError("Passwords do not match")

#         try:
#             validate_password(attrs["password"])
#         except DjangoValidationError as e:
#             raise serializers.ValidationError(e.messages)

#         return attrs




