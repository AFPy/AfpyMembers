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


    def test_letters(self):
        resp = self.app.get(url(controller='admin',
                                action='letters', id='all'),
                                extra_environ=admin_environ)
        resp.mustcontain('A', 'B', 'Z')

        resp = self.app.get(url(controller='admin',
                                action='letters', id='subscribers'),
                                extra_environ=admin_environ)
        resp.mustcontain('A', 'B', 'Z')

        resp = self.app.get(url(controller='admin',
                                action='letters', id='membres'),
                                extra_environ=admin_environ)
        resp.mustcontain('A', 'B', 'Z')

    def test_listes(self):
        resp = self.app.get(url(controller='admin',
                                action='subscribers', stype='all',
                                letter='g'),
                                extra_environ=admin_environ)
        resp.mustcontain('gawel', 'infos', '+')

        resp = self.app.get(url(controller='admin',
                                action='subscribers', stype='subscribers',
                                letter='g'),
                                extra_environ=admin_environ)
        resp.mustcontain('gawel', 'infos', '+')

        resp = self.app.get(url(controller='admin',
                                action='subscribers', stype='membres',
                                letter='g'),
                                extra_environ=admin_environ)
        resp.mustcontain('infos', '+')

        resp = self.app.post(url(controller='admin',
                                action='subscribers', stype='search',
                                letter='all'),
                                dict(letter='pasgrimaud'),
                                extra_environ=admin_environ)
        resp.mustcontain('gawel', 'infos', '+')


