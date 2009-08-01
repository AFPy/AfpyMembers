from members.tests import *

class TestUtilsController(TestController):

    def test_personnal_bar(self):
        resp = self.app.get(url(controller='utils', action='personnal_bar'))
        resp.mustcontain('/register', '/login')

        resp = self.app.get(url(controller='utils', action='personnal_bar'),
                            extra_environ=admin_environ)
        resp.mustcontain('gawel', '/logout')

