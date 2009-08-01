from members.tests import *

class TestMapsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='maps', action='datas'))
        response.mustcontain('{"result": [')
