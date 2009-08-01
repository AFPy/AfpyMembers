from members.tests import *

class TestAdminController(TestController):

    def test_index(self):
        resp = self.app.get(url(controller='admin', action='new'),
                                extra_environ=admin_environ)
        resp.mustcontain('AfpyUser--uid')

        form = resp.forms['new_user']
        form['AfpyUser--uid'] = 'afpytestuser'
        resp = form.submit(extra_environ=admin_environ)

        resp.mustcontain('Vous devez saisir une valeur')
