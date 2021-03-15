"""
Tests for the workouts application.
"""
from django.test import TestCase, Client
from datetime import datetime
from .permissions import IsOwner, IsPublic, IsReadOnly, IsCoachAndVisibleToCoach, IsCoachOfWorkoutAndVisibleToCoach, IsOwnerOfWorkout, IsWorkoutPublic
from .mock import MockRequest, MockView, MockWorkout, MockOwner, MockWorkoutWithCoach, MockCoachRequest
from .models import Workout
from django.contrib.auth import get_user_model
import copy
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


# Create your tests here.


class WorkoutsPermissionsTestCase(TestCase):

    # Test data for a workout
    workoutData = {
        "name": "testName",
        "date": datetime.now(),
        "notes": "testNotes",
        "owner": "John",
        "visibility": "PU"
    }

    # Test data for a user
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

        # Initializing permission classes
        self.isOwner = IsOwner()
        self.isPublic = IsPublic()
        self.isReadOnly = IsReadOnly()
        self.isCoachAndVisibleToCoach = IsCoachAndVisibleToCoach()
        self.isCoachOfWorkoutAndVisibleToCoach = IsCoachOfWorkoutAndVisibleToCoach()
        self.isOwnerOfWorkout = IsOwnerOfWorkout()
        self.isWorkoutPublic = IsWorkoutPublic()

        # Initializing simple requests (Requests where only the user of the request is relevant)
        self.simple_request = MockRequest()
        self.simple_safe_request = MockRequest()
        self.simple_faulty_request = MockRequest()
        self.simple_faulty_request.user = "Jonathan13"
        self.simple_safe_request.method = "GET"

        # Initializing simple coach requests
        self.simple_coach_request = MockCoachRequest()
        self.simple_faulty_coach_request = MockCoachRequest()
        self.simple_faulty_coach_request.user = "Hannah"

        # Initializing complex request (Request where more than just the user is relevant)
        self.complex_request = MockRequest()

        # Initializing view and object
        self.view = MockView()
        self.obj = MockWorkout()
        self.obj_faulty = MockWorkout()
        self.obj.workout = MockWorkout()
        self.obj_faulty.workout = MockWorkout()
        self.obj_faulty.workout.visibility = "PR"
        self.obj_faulty.visibility = "PR"

        # Initializing workout with coach
        self.obj_coach = MockWorkoutWithCoach()
        self.obj_coach.owner = MockOwner()
        self.obj_coach.workout = MockWorkoutWithCoach()
        self.obj_coach.workout.owner = MockWorkoutWithCoach()
        self.obj_coach.owner.coach = "Peter"
        self.obj_coach.workout.owner.coach = "Peter"

        # Initializing and saving test-user
        user_obj = get_user_model()(username=self.userData["username"], email=self.userData["email"],
                                    phone_number=self.userData["phone_number"], country=self.userData["country"],
                                    city=self.userData["city"], street_address=self.userData["street_address"])
        user_obj.save()

        # Initializing and saving test-workout
        self.workoutData["owner"] = user_obj
        Workout.objects.create(**self.workoutData)

        # Filling the complex request with necessary data (Test user and Test data)
        self.complex_request.data["workout"] = "01/Workout"
        self.complex_request.user = user_obj

    def test_is_owner(self):
        self.assertTrue(self.isOwner.has_object_permission(self.simple_request, self.view, self.obj))
        self.assertFalse(self.isOwner.has_object_permission(self.simple_faulty_request, self.view, self.obj))

    def test_is_owner_of_workout(self):

        # The "has_permission" function receives the complex request as it depends on data and an actual user instance
        # to be able to extract the corresponding workout from the database and test the permission correctly
        self.assertTrue(self.isOwnerOfWorkout.has_permission(self.complex_request, self.view))

        self.assertTrue(self.isOwnerOfWorkout.has_object_permission(self.simple_request, self.view, self.obj))
        self.assertFalse(self.isOwner.has_object_permission(self.simple_faulty_request, self.view, self.obj))

    def test_is_coach_and_visible_to_coach(self):
        self.assertTrue(self.isCoachAndVisibleToCoach.has_object_permission(self.simple_coach_request, self.view, self.obj_coach))
        self.assertFalse(self.isCoachAndVisibleToCoach.has_object_permission(self.simple_faulty_coach_request, self.view, self.obj_coach))

    def test_is_coach_of_workout_and_visible_to_coach(self):
        self.assertTrue(self.isCoachOfWorkoutAndVisibleToCoach.has_object_permission(self.simple_coach_request, self.view, self.obj_coach))
        self.assertFalse(self.isCoachOfWorkoutAndVisibleToCoach.has_object_permission(self.simple_faulty_coach_request, self.view, self.obj_coach))

    def test_is_public(self):
        self.assertTrue(self.isPublic.has_object_permission(self.simple_request, self.view, self.obj))
        self.assertFalse(self.isPublic.has_object_permission(self.simple_request, self.view, self.obj_faulty))

    def test_is_workout_public(self):
        self.assertTrue(self.isWorkoutPublic.has_object_permission(self.simple_request, self.view, self.obj))
        self.assertFalse(self.isWorkoutPublic.has_object_permission(self.simple_request, self.view, self.obj_faulty))

    def test_is_read_only(self):
        self.assertTrue(self.isReadOnly.has_object_permission(self.simple_safe_request, self.view, self.obj))
        self.assertFalse(self.isReadOnly.has_object_permission(self.simple_request, self.view, self.obj))


# class CreateWorkoutBoundaryTesting(TestCase):
#
#     workoutData_known_to_be_legal = {
#         "url": "",
#         "id": "",
#         "name": "",
#         "date": "",
#         "notes": "",
#         "owner": "",
#         "owner_username": "",
#         "visibility": "",
#         "exercise_instances": "",
#         "files": "",
#     }
#
#     userData = {
#         "username": "test",
#         "email": "thom_as@coldmail.com",
#         "password": "test123",
#         "phone_number": "asdasdasd",
#         "country": "NoMansLand",
#         "city": "Capitalum",
#         "street_address": "221B Baker Street",
#         "password1": "asd",
#         "athletes": {},
#         "coach": "",
#         "workouts": {},
#         "coach_files": {},
#         "athlete_files": {}
#     }
#
#     workoutData = {}
#
#     def setUp(self):
#         self.client = APIClient()
#
#         user = User.objects.create_user(username="test", email="a@a.com", password='test123')
#         refresh = RefreshToken.for_user(user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + refresh.access_token)
#
#         self.workoutData = copy.deepcopy(self.workoutData_known_to_be_legal)
#         response = self.client.post("http://localhost:8000/api/workouts/", self.workoutData, "json")
#         print(response.json())
#
#     def test_something(self):
#         self.assertTrue(True)
#
#     # def test_name(self):
#     #     eq_domain = {
#     #         "characters": "thomas",
#     #         "integers": "123456",
#     #         "symbols": "&%_#",
#     #         "empty": "",
#     #         "space": " ",
#     #         "characters_integers_symbols": "thomas46&%",
#     #         "characters_and_space": "thomas lingon",
#     #         "short": "a",
#     #         "long": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
#     #     }
#     #
#     #     self.userData = copy.deepcopy(self.userData_known_to_be_legal)
#     #
#     #     self.userData["email"] = "ra@a.com"
#     #     self.userData["username"] = eq_domain["characters"]
#     #     response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
#     #     self.assertEquals(response.status_code, 201)
#     #
#     #     self.userData["email"] = "raa@a.com"
#     #     self.userData["username"] = eq_domain["integers"]
#     #     response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
#     #     self.assertEquals(response.status_code, 201)
#     #
#     #     self.userData["email"] = "raaa@a.com"
#     #     self.userData["username"] = eq_domain["symbols"]
#     #     response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
#     #     self.assertEquals(response.status_code, 400)
#     #
#     #     self.userData["email"] = "raaaa@a.com"
#     #     self.userData["username"] = eq_domain["empty"]
#     #     response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
#     #     self.assertEquals(response.status_code, 400)
#     #
#     #     self.userData["email"] = "raaaaa@a.com"
#     #     self.userData["username"] = eq_domain["space"]
#     #     response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
#     #     self.assertEquals(response.status_code, 400)
#     #
#     #     self.userData["email"] = "raaaaaa@a.com"
#     #     self.userData["username"] = eq_domain["characters_integers_symbols"]
#     #     response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
#     #     self.assertEquals(response.status_code, 400)
#     #
#     #     self.userData["email"] = "raaaaaaa@a.com"
#     #     self.userData["username"] = eq_domain["characters_and_space"]
#     #     response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
#     #     self.assertEquals(response.status_code, 400)
#     #
#     #     self.userData["email"] = "raaaaaaaa@a.com"
#     #     self.userData["username"] = eq_domain["short"]
#     #     response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
#     #     self.assertEquals(response.status_code, 201)
#     #
#     #     self.userData["email"] = "raaaaaaaaa@a.com"
#     #     self.userData["username"] = eq_domain["long"]
#     #     response = self.client.post("http://localhost:8000/api/users/", self.userData, "application/json")
#     #     self.assertEquals(response.status_code, 201)
#     #
#     # def test_date(self):
#     #
#     # def test_visibility(self):
#     #
#     # def test_notes(self):
#     #
#     # def test_files(self):
#     #
#     # def test_exerciseInstances(self):
#     #
