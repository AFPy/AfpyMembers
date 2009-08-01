from members.tests import *

class TestPaymentsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='payments'),
                                extra_environ=admin_environ)
        response.mustcontain('Mes paiements')

    def test_edit(self):
        response = self.app.get(url(controller='payments',
                                action='edit', id='ogrisel'),
                                extra_environ=admin_environ)
        response.mustcontain('/edit', '>Sauver</a>')


