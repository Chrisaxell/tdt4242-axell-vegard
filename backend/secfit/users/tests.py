from django.test import TestCase, Client
from .serializers import UserSerializer
from .models import User
from .views import UserList
from .mock import MockRequest
import copy

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


class SignUpBoundaryTesting(TestCase):

    userData_known_to_be_legal = {
        "username": "asdasd",
        "email": "thom_as@coldmail.com",
        "password": "wordpass321",
        "phone_number": "asdasdasd",
        "country": "NoMansLand",
        "city": "Capitalum",
        "street_address": "221B Baker Street",
        "password1": "asd",
        "athletes": {},
        "coach": "",
        "workouts": {},
        "coach_files": {},
        "athlete_files": {}
    }

    userData = {}

    def setUp(self):
        self.client = Client()

    def test_username(self):

        eq_domain = {
            "characters": "thomas",
            "integers": "123456",
            "symbols": "&%_#",
            "empty": "",
            "space": " ",
            "characters_integers_symbols": "thomas46&%",
            "characters_and_space": "thomas lingon",
            "short": "a",
            "long": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        }

        self.userData = copy.deepcopy(self.userData_known_to_be_legal)

        self.userData["email"] = "ra@a.com"
        self.userData["username"] = eq_domain["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["email"] = "raa@a.com"
        self.userData["username"] = eq_domain["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["email"] = "raaa@a.com"
        self.userData["username"] = eq_domain["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["email"] = "raaaa@a.com"
        self.userData["username"] = eq_domain["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["email"] = "raaaaa@a.com"
        self.userData["username"] = eq_domain["space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["email"] = "raaaaaa@a.com"
        self.userData["username"] = eq_domain["characters_integers_symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["email"] = "raaaaaaa@a.com"
        self.userData["username"] = eq_domain["characters_and_space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["email"] = "raaaaaaaa@a.com"
        self.userData["username"] = eq_domain["short"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["email"] = "raaaaaaaaa@a.com"
        self.userData["username"] = eq_domain["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        

    def test_email(self):

        eq_domain = {
            "characters": "a@a.com",
            "integers": "1@1.com",
            "symbols": "&@&.com",
            "empty": "",
            "space": "a @a.com",
            "characters_and_underscore": "a_a@a.com",
            "characters_and_symbols": "a&a@aa.com",
            "long": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@aaaaaaaaaaaaaaaaaaaaaaaaaaa.com",
            "without_alpha": "aaaaa.com",
            "without_domain": "a@a",
            "without_both": "aaa"
        }

        self.userData = copy.deepcopy(self.userData_known_to_be_legal)

        self.userData["username"] = "a"
        self.userData["email"] = eq_domain["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "aa"
        self.userData["email"] = eq_domain["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "aaa"
        self.userData["email"] = eq_domain["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "aaaa"
        self.userData["email"] = eq_domain["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "aaaaa"
        self.userData["email"] = eq_domain["space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "aaaaaa"
        self.userData["email"] = eq_domain["characters_and_underscore"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "aaaaaaa"
        self.userData["email"] = eq_domain["characters_and_symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "aaaaaaaa"
        self.userData["email"] = eq_domain["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "aaaaaaaaa"
        self.userData["email"] = eq_domain["without_alpha"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "aaaaaaaaaa"
        self.userData["email"] = eq_domain["without_domain"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "aaaaaaaaaaa"
        self.userData["email"] = eq_domain["without_both"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)
        

    def test_password(self):

        eq_domain = {
            "characters": "thomas",
            "integers": "123456",
            "symbols": "&%_#",
            "empty": "",
            "space": " ",
            "characters_integers_symbols": "thomas46&%",
            "characters_and_space": "thomas lingon",
            "short": "a",
            "long": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        }

        self.userData = copy.deepcopy(self.userData_known_to_be_legal)

        self.userData["username"] = "wa"
        self.userData["email"] = "wa@a.com"
        self.userData["password"] = eq_domain["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "waa"
        self.userData["email"] = "waa@a.com"
        self.userData["password"] = eq_domain["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "waaa"
        self.userData["email"] = "waaa@a.com"
        self.userData["password"] = eq_domain["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "waaaa"
        self.userData["email"] = "waaaa@a.com"
        self.userData["password"] = eq_domain["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)
        
        self.userData["username"] = "waaaaa"
        self.userData["email"] = "waaaaa@a.com"
        self.userData["password"] = eq_domain["space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)
        
        self.userData["username"] = "waaaaaa"
        self.userData["email"] = "waaaaaa@a.com"
        self.userData["password"] = eq_domain["characters_integers_symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "waaaaaaa"
        self.userData["email"] = "waaaaaaa@a.com"
        self.userData["password"] = eq_domain["characters_and_space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "waaaaaaaa"
        self.userData["email"] = "waaaaaaaa@a.com"
        self.userData["password"] = eq_domain["short"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "waaaaaaaaa"
        self.userData["email"] = "waaaaaaaaa@a.com"
        self.userData["password"] = eq_domain["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        

    def test_phonenumber(self):

        eq_domain = {
            "characters": "thomas",
            "integers": "123456",
            "symbols": "&%_#",
            "empty": "",
            "space": " ",
            "integers_and_space": "1234 1243",
            "symbols_and_integers": "+4712341234",
            "short": "1",
            "long": "111111111111111111111111111111111111111111111111111"
        }

        self.userData = copy.deepcopy(self.userData_known_to_be_legal)

        self.userData["username"] = "ma"
        self.userData["email"] = "ma@a.com"
        self.userData["phone_number"] = eq_domain["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "maa"
        self.userData["email"] = "maa@a.com"
        self.userData["phone_number"] = eq_domain["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "maaa"
        self.userData["email"] = "maaa@a.com"
        self.userData["phone_number"] = eq_domain["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "maaaa"
        self.userData["email"] = "maaaa@a.com"
        self.userData["phone_number"] = eq_domain["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "maaaaa"
        self.userData["email"] = "maaaaa@a.com"
        self.userData["phone_number"] = eq_domain["space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "maaaaaa"
        self.userData["email"] = "maaaaaa@a.com"
        self.userData["phone_number"] = eq_domain["symbols_and_integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "maaaaaaa"
        self.userData["email"] = "maaaaaaa@a.com"
        self.userData["phone_number"] = eq_domain["integers_and_space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "maaaaaaaa"
        self.userData["email"] = "maaaaaaaa@a.com"
        self.userData["phone_number"] = eq_domain["short"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "maaaaaaaaa"
        self.userData["email"] = "maaaaaaaaa@a.com"
        self.userData["phone_number"] = eq_domain["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)
        

    def test_country(self):

        eq_domain = {
            "characters": "thomas",
            "integers": "123456",
            "symbols": "&%_#",
            "empty": "",
            "space": " ",
            "characters_and_space": "republic of something",
            "short": "a",
            "long": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        }

        self.userData = copy.deepcopy(self.userData_known_to_be_legal)

        self.userData["username"] = "ua"
        self.userData["email"] = "ua@a.com"
        self.userData["country"] = eq_domain["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "uaa"
        self.userData["email"] = "uaa@a.com"
        self.userData["country"] = eq_domain["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "uaaa"
        self.userData["email"] = "uaaa@a.com"
        self.userData["country"] = eq_domain["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "uaaaa"
        self.userData["email"] = "uaaaa@a.com"
        self.userData["country"] = eq_domain["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "uaaaaa"
        self.userData["email"] = "uaaaaa@a.com"
        self.userData["country"] = eq_domain["space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "uaaaaaa"
        self.userData["email"] = "uaaaaaa@a.com"
        self.userData["country"] = eq_domain["characters_and_space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "uaaaaaaa"
        self.userData["email"] = "uaaaaaaa@a.com"
        self.userData["country"] = eq_domain["short"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "uaaaaaaaa"
        self.userData["email"] = "uaaaaaaaa@a.com"
        self.userData["country"] = eq_domain["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        

    def test_city(self):

        eq_domain = {
            "characters": "thomas",
            "integers": "123456",
            "symbols": "&%_#",
            "empty": "",
            "space": " ",
            "characters_and_space": "republic of something",
            "characters_and_symbol": "green-country",
            "short": "a",
            "long": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        }

        self.userData = copy.deepcopy(self.userData_known_to_be_legal)

        self.userData["username"] = "ya"
        self.userData["email"] = "ya@a.com"
        self.userData["city"] = eq_domain["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "yaa"
        self.userData["email"] = "yaa@a.com"
        self.userData["city"] = eq_domain["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "yaaa"
        self.userData["email"] = "yaaa@a.com"
        self.userData["city"] = eq_domain["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "yaaaa"
        self.userData["email"] = "yaaaa@a.com"
        self.userData["city"] = eq_domain["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "yaaaaa"
        self.userData["email"] = "yaaaaa@a.com"
        self.userData["city"] = eq_domain["space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "yaaaaaa"
        self.userData["email"] = "yaaaaaa@a.com"
        self.userData["city"] = eq_domain["characters_and_space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "yaaaaaaa"
        self.userData["email"] = "yaaaaaaa@a.com"
        self.userData["city"] = eq_domain["characters_and_symbol"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "yaaaaaaaa"
        self.userData["email"] = "yaaaaaaaa@a.com"
        self.userData["city"] = eq_domain["short"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "yaaaaaaaaa"
        self.userData["email"] = "yaaaaaaaaa@a.com"
        self.userData["city"] = eq_domain["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        

    def test_street_address(self):

        eq_domain = {
            "characters": "thomas",
            "integers": "123456",
            "symbols": "&%_#",
            "empty": "",
            "space": " ",
            "characters_and_space": "republic of something",
            "characters_and_symbol": "green-country",
            "characters_and_integers": "1B",
            "characters_symbols_and_integers": "1-B",
            "characters_integers_and_space": "Downing 1B",
            "short": "a",
            "long": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        }

        self.userData = copy.deepcopy(self.userData_known_to_be_legal)

        self.userData["username"] = "sa"
        self.userData["email"] = "sa@a.com"
        self.userData["street_address"] = eq_domain["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saa"
        self.userData["email"] = "saa@a.com"
        self.userData["street_address"] = eq_domain["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaa"
        self.userData["email"] = "saaa@a.com"
        self.userData["street_address"] = eq_domain["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaaa"
        self.userData["email"] = "saaaa@a.com"
        self.userData["street_address"] = eq_domain["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaaaa"
        self.userData["email"] = "saaaaa@a.com"
        self.userData["street_address"] = eq_domain["space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaaaaa"
        self.userData["email"] = "saaaaaa@a.com"
        self.userData["street_address"] = eq_domain["characters_and_space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaaaaaa"
        self.userData["email"] = "saaaaaaa@a.com"
        self.userData["street_address"] = eq_domain["characters_and_symbol"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaaaaaaa"
        self.userData["email"] = "saaaaaaaa@a.com"
        self.userData["street_address"] = eq_domain["characters_and_integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaaaaaaaa"
        self.userData["email"] = "saaaaaaaaa@a.com"
        self.userData["street_address"] = eq_domain["characters_symbols_and_integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaaaaaaaaa"
        self.userData["email"] = "saaaaaaaaaa@a.com"
        self.userData["street_address"] = eq_domain["characters_integers_and_space"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaaaaaaaaaa"
        self.userData["email"] = "saaaaaaaaaaa@a.com"
        self.userData["street_address"] = eq_domain["short"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        
        self.userData["username"] = "saaaaaaaaaaaa"
        self.userData["email"] = "saaaaaaaaaaaa@a.com"
        self.userData["street_address"] = eq_domain["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)
        

class TwoWayTestPhonenumberAndPassword(TestCase):

    userData = {
        "username": "asdasd",
        "email": "thom_as@coldmail.com",
        "password": "wordpass321",
        "phone_number": "asdasdasd",
        "country": "NoMansLand",
        "city": "Capitalum",
        "street_address": "221B Baker Street",
        "password1": "asd",
        "athletes": {},
        "coach": "",
        "workouts": {},
        "coach_files": {},
        "athlete_files": {}
    }

    def setUp(self):
        self.client = Client()

    def test_username(self):
        eq_domain_password = {
            "characters": "a",
            "integers": "123456",
            "symbols": "&%_#",
            "empty": "",
            "long": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        }

        eq_domain_phonenumber = {
            "characters": "a",
            "integers": "123456",
            "symbols": "&%_#",
            "empty": "",
            "long": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
        }

        self.userData["username"] = "sa"
        self.userData["email"] = "sa@a.com"
        self.userData["password"] = eq_domain_password["characters"]
        self.userData["phone_number"] = eq_domain_phonenumber["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "saa"
        self.userData["email"] = "saa@a.com"
        self.userData["password"] = eq_domain_password["characters"]
        self.userData["phone_number"] = eq_domain_phonenumber["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "saaa"
        self.userData["email"] = "saaa@a.com"
        self.userData["password"] = eq_domain_password["characters"]
        self.userData["phone_number"] = eq_domain_phonenumber["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "saaaa"
        self.userData["email"] = "saaaa@a.com"
        self.userData["password"] = eq_domain_password["characters"]
        self.userData["phone_number"] = eq_domain_phonenumber["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "saaaaa"
        self.userData["email"] = "saaaaa@a.com"
        self.userData["password"] = eq_domain_password["characters"]
        self.userData["phone_number"] = eq_domain_phonenumber["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "saaaaaa"
        self.userData["email"] = "saaaaaa@a.com"
        self.userData["password"] = eq_domain_password["integers"]
        self.userData["phone_number"] = eq_domain_phonenumber["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "saaaaaaa"
        self.userData["email"] = "saaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["integers"]
        self.userData["phone_number"] = eq_domain_phonenumber["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "saaaaaaaa"
        self.userData["email"] = "saaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["integers"]
        self.userData["phone_number"] = eq_domain_phonenumber["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "saaaaaaaaa"
        self.userData["email"] = "saaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["integers"]
        self.userData["phone_number"] = eq_domain_phonenumber["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "saaaaaaaaaa"
        self.userData["email"] = "saaaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["integers"]
        self.userData["phone_number"] = eq_domain_phonenumber["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "saaaaaaaaaaa"
        self.userData["email"] = "saaaaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["symbols"]
        self.userData["phone_number"] = eq_domain_phonenumber["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "saaaaaaaaaaaa"
        self.userData["email"] = "saaaaaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["symbols"]
        self.userData["phone_number"] = eq_domain_phonenumber["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "xa"
        self.userData["email"] = "xa@a.com"
        self.userData["password"] = eq_domain_password["symbols"]
        self.userData["phone_number"] = eq_domain_phonenumber["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "xaa"
        self.userData["email"] = "xaa@a.com"
        self.userData["password"] = eq_domain_password["symbols"]
        self.userData["phone_number"] = eq_domain_phonenumber["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "xaaa"
        self.userData["email"] = "xaaa@a.com"
        self.userData["password"] = eq_domain_password["symbols"]
        self.userData["phone_number"] = eq_domain_phonenumber["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "xaaaa"
        self.userData["email"] = "xaaaa@a.com"
        self.userData["password"] = eq_domain_password["empty"]
        self.userData["phone_number"] = eq_domain_phonenumber["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "xaaaaa"
        self.userData["email"] = "xaaaaa@a.com"
        self.userData["password"] = eq_domain_password["empty"]
        self.userData["phone_number"] = eq_domain_phonenumber["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "xaaaaaaa"
        self.userData["email"] = "xaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["empty"]
        self.userData["phone_number"] = eq_domain_phonenumber["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "xaaaaaaaa"
        self.userData["email"] = "xaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["empty"]
        self.userData["phone_number"] = eq_domain_phonenumber["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "xaaaaaaaaa"
        self.userData["email"] = "xaaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["empty"]
        self.userData["phone_number"] = eq_domain_phonenumber["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)

        self.userData["username"] = "xaaaaaaaaaa"
        self.userData["email"] = "xaaaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["long"]
        self.userData["phone_number"] = eq_domain_phonenumber["characters"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "xaaaaaaaaaaa"
        self.userData["email"] = "xaaaaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["long"]
        self.userData["phone_number"] = eq_domain_phonenumber["integers"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "qaaaaaaaaaaaa"
        self.userData["email"] = "qaaaaaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["long"]
        self.userData["phone_number"] = eq_domain_phonenumber["symbols"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "qaaaaaaaaaaaaa"
        self.userData["email"] = "qaaaaaaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["long"]
        self.userData["phone_number"] = eq_domain_phonenumber["empty"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 201)

        self.userData["username"] = "qaaaaaaaaaaaaaa"
        self.userData["email"] = "qaaaaaaaaaaaaaa@a.com"
        self.userData["password"] = eq_domain_password["long"]
        self.userData["phone_number"] = eq_domain_phonenumber["long"]
        response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
        self.assertEquals(response.status_code, 400)




