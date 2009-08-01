from members.tests import *

class TestAdminController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='admin'),
                                extra_environ=admin_environ)
