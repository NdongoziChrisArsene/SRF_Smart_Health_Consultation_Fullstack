from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="pass1234"
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("pass1234"))
        self.assertEqual(user.role, "patient")

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="admin1234"
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, "admin")
































# from django.test import TestCase
# from .models import User


# class UserTests(TestCase):
#     def test_create_user(self):
#         user = User.objects.create_user(
#             username="testuser",
#             email="a@b.com",
#             password="pass1234"
#         )
#         self.assertEqual(user.username, "testuser")
#         self.assertTrue(user.check_password("pass1234"))











































# from django.test import TestCase
# from .models import User

# class UserTests(TestCase):
#     def test_create_user(self):
#         user = User.objects.create_user(username="test", email="a@b.com", password="pass")
#         self.assertEqual(user.username, "test")
