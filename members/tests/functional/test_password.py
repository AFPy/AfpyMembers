from members.tests import *

class TestPasswordController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='password'))
        # Test response...
