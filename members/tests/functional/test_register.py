from members.tests import *
from afpy.ldap import custom as ldap

class TestRegisterController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='register',
                                        action='register_form'))
        form = response.forms[0]
        form['AfpyUser--uid'] = 'gawel'
        form['AfpyUser--mail'] = 'afpy@gawel.org'
        form['AfpyUser--password'] = 'toto'
        response = form.submit('validate')
        assert 'Cet identifiant est pris' in response, response

        form['AfpyUser--uid'] = 'afpy_test_user'
        form['AfpyUser--mail'] = 'afpy@gawel.org'
        form['AfpyUser--password'] = 'toto'
        response = form.submit('validate')
        assert 'Cet email est pris' in response, response

        form['AfpyUser--uid'] = 'afpy_test_user'
        form['AfpyUser--mail'] = 'afpy@gawel.org'
        form['AfpyUser--password'] = 'toto'
        response = form.submit('validate')
        assert 'Cet email est pris' in response, response

        form['AfpyUser--uid'] = 'Afpy_Test_User'
        form['AfpyUser--sn'] = 'Afpy User'
        form['AfpyUser--mail'] = 'test@afpy.org'
        form['AfpyUser--password'] = 'toto'
        response = form.submit('validate')
        response.mustcontain('Votre inscription', 'Vous allez recevoir')

        user = ldap.getUser('afpy_test_user')
        assert user is not None

        response = self.app.get(url(controller='register', action='confirm', uid=user.uid, key=user.street))

        user.conn.delete(user)
        assert ldap.getUser('afpy_test_user') is None
