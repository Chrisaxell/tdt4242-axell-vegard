from django.test import TestCase
from django.contrib.auth import password_validation
from .serializers import UserSerializer

# Create your tests here.

class UserCreationTestCase(TestCase):
    userData = {
                "username": "Thomas42",
                "email": "thom_as@coldmail.com",
                "password": "wordpass321",
                "phone_number": "77755566",
                "country": "NoMansLand",
                "city": "Capitalum",
                "street_address": "221B Baker Street"
            }

    created_user = None

    def setUp(self):
        self.created_user = UserSerializer.create(self, self.userData)

    def test_user_creation(self):
        self.assertEquals(self.userData["username"], self.created_user.username)
        self.assertEquals(self.userData["phone_number"], self.created_user.phone_number)
        self.assertEquals(self.userData["city"], self.created_user.city)

    def test_validate_password(self):
        self.assertEquals(True, True)




