from members.tests import *

class TestMyController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='my',
                                        action='info', id='gawel'),
                                extra_environ=admin_environ)
        form = response.forms[0]
        response = form.submit('save', extra_environ=admin_environ)
        assert 'Modifie -' in response, response


    def test_letters(self):
        resp = self.app.get(url(controller='my',
                                action='letters', id='all'),
                                extra_environ=admin_environ)
        resp.mustcontain('A', 'B', 'Z')

        resp = self.app.get(url(controller='my',
                                action='letters', id='subscribers'),
                                extra_environ=admin_environ)
        resp.mustcontain('A', 'B', 'Z')

        resp = self.app.get(url(controller='my',
                                action='letters', id='membres'),
                                extra_environ=admin_environ)
        resp.mustcontain('A', 'B', 'Z')

    def test_listes(self):
        resp = self.app.get(url(controller='my',
                                action='subscribers', stype='all',
                                letter='g'),
                                extra_environ=admin_environ)
        resp.mustcontain('gawel', 'infos', '+')

        resp = self.app.get(url(controller='my',
                                action='subscribers', stype='subscribers',
                                letter='g'),
                                extra_environ=admin_environ)
        resp.mustcontain('gawel', 'infos', '+')

        resp = self.app.get(url(controller='my',
                                action='subscribers', stype='membres',
                                letter='g'),
                                extra_environ=admin_environ)
        resp.mustcontain('infos', '+')

        resp = self.app.post(url(controller='my',
                                action='subscribers', stype='search',
                                letter='all'),
                                dict(letter='gael'),
                                extra_environ=admin_environ)
        resp.mustcontain('gawel', 'infos', '+')

