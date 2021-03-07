"""
Tests for the workouts application.
"""
from django.test import TestCase
from datetime import datetime
from .permissions import IsOwner, IsPublic, IsReadOnly, IsCoachAndVisibleToCoach, IsCoachOfWorkoutAndVisibleToCoach, IsOwnerOfWorkout, IsWorkoutPublic
from .mock import MockRequest, MockView, MockWorkout
from .models import Workout
from django.contrib.auth import get_user_model


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
        self.simple_faulty_request = MockRequest()
        self.simple_faulty_request.user = "Jonathan13"

        # Initializing complex request (Request where more than just the user is relevant)
        self.complex_request = MockRequest()

        # Initializing view and object
        self.view = MockView()
        self.obj = MockWorkout()
        self.obj.workout = MockWorkout()

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

    # def test_is_coach_and_visible_to_coach(self):
    #     self.assertTrue(self.isOwner.has_object_permission(self.request, self.view, self.obj))
    #     self.assertFalse(self.isOwner.has_object_permission(self.request, self.view, self.obj))
    #
    # def test_is_coach_of_workout_and_visible_to_coach(self):
    #     self.assertTrue(self.isOwner.has_object_permission(self.request, self.view, self.obj))
    #     self.assertFalse(self.isOwner.has_object_permission(self.request, self.view, self.obj))
    #
    # def test_is_public(self):
    #     self.assertTrue(self.isOwner.has_object_permission(self.request, self.view, self.obj))
    #     self.assertFalse(self.isOwner.has_object_permission(self.request, self.view, self.obj))
    #
    # def test_is_workout_public(self):
    #     self.assertTrue(self.isOwner.has_object_permission(self.request, self.view, self.obj))
    #     self.assertFalse(self.isOwner.has_object_permission(self.request, self.view, self.obj))
    #
    # def test_is_read_only(self):
    #     self.assertTrue(self.isOwner.has_object_permission(self.request, self.view, self.obj))
    #     self.assertFalse(self.isOwner.has_object_permission(self.request, self.view, self.obj))

