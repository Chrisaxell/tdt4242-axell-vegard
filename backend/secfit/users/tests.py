from django.test import TestCase
from .serializers import UserSerializer
from .models import User

# Create your tests here.


class UserCreationTestCase(TestCase):

    # Test data for test user
    userData = {
                "username": "Thomas42",
                "email": "thom_as@coldmail.com",
                "password": "wordpass321",
                "phone_number": "77755566",
                "country": "NoMansLand",
                "city": "Capitalum",
                "street_address": "221B Baker Street"
            }

    def setUp(self):

        # Initializing user serializer
        self.serializer = UserSerializer()

        # Create an entry of a user using the user-serializer
        self.serializer.create(self.userData)

        # Retrieve the newly created user using its primary key
        self.saved_user = User.objects.get(pk=1)

    def test_user_creation_and_storage(self):

        # We test that the integrity of the userData is preserved through serialization, saving and retrieval
        self.assertEquals(self.userData["username"], self.saved_user.username)
        self.assertEquals(self.userData["phone_number"], self.saved_user.phone_number)
        self.assertEquals(self.userData["city"], self.saved_user.city)

    def test_validate_password(self):

        # We test that the password validation validates the correct password, but rejects a faulty password
        self.assertEquals(self.serializer.validate_password(self.userData["password"]), self.userData["password"])
        self.assertNotEqual(self.serializer.validate_password("WrongPassword"), self.userData["password"])




