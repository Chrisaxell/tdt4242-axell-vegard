
class MockRequest(object):
    user = "Thomas42"
    method = "POST"
    data = {"workout": None}


class MockCoachRequest(object):
    user = "Peter"


class MockView(object):
    pass


class MockWorkout(object):
    owner = "Thomas42"
    workout = None
    visibility = "PU"


class MockWorkoutWithCoach(object):
    owner = None
    workout = None


class MockOwner(object):
    coach = "Peter"
