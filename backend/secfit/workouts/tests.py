"""
Tests for the workouts application.
"""
from django.test import TestCase
from rest_framework import permissions
from workouts.models import Workout

# Create your tests here.


class WorkoutsPermissionsTestCase(TestCase):

    variable = 1

    def setUp(self):
        self.variable = 2

    def test_is_owner(self):
        self.assertEqual(self.variable, 2)

    def test_is_owner_of_workout(self):
        self.assertEqual(self.variable, 2)

    def test_is_coach_and_visible_to_coach(self):
        self.assertEqual(self.variable, 2)

    def test_is_coach_of_workout_and_visible_to_coach(self):
        self.assertEqual(self.variable, 2)

    def test_is_public(self):
        self.assertEqual(self.variable, 2)

    def test_is_workout_public(self):
        self.assertEqual(self.variable, 2)

    def test_is_read_only(self):
        self.assertEqual(self.variable, 2)

