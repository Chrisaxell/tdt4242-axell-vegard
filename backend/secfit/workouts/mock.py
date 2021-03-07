
class MockRequest(object):
    user = "Thomas42"
    method = "POST"
    data = {"workout": None}


class MockView(object):
    pass


class MockWorkout(object):
    owner = "Thomas42"
    workout = None
