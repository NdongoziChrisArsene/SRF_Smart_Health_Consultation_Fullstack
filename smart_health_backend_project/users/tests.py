from django.test import TestCase
from .models import User


class UserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="a@b.com",
            password="pass1234"
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("pass1234"))











































# from django.test import TestCase
# from .models import User

# class UserTests(TestCase):
#     def test_create_user(self):
#         user = User.objects.create_user(username="test", email="a@b.com", password="pass")
#         self.assertEqual(user.username, "test")
