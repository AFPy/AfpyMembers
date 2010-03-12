from members.tests import *
from afpy.ldap import custom as ldap

class TestRegisterController(TestController):

    def test_index(self):
        response = self.app.post(url(controller='register',
                                        action='register_form'))
        form = response.forms[0]
        form['User--uid'] = 'gawel'
        form['User--mail'] = 'afpy@gawel.org'
        form['User--password'] = 'toto'
        response = form.submit('validate')
        assert 'Cet identifiant est pris' in response, response

        form['User--uid'] = 'afpy_test_user'
        form['User--mail'] = 'afpy@gawel.org'
        form['User--password'] = 'toto'
        response = form.submit('validate')
        assert 'Cet email est pris' in response, response

        form['User--uid'] = 'afpy_test_user'
        form['User--mail'] = 'afpy@gawel.org'
        form['User--password'] = 'toto'
        response = form.submit('validate')
        assert 'Cet email est pris' in response, response

        form['User--uid'] = 'Afpy_Test_User'
        form['User--sn'] = 'Afpy User'
        form['User--mail'] = 'test@afpy.org'
        form['User--password'] = 'toto'
        response = form.submit('validate')
        response.mustcontain('Votre inscription', 'Vous allez recevoir')

        user = ldap.getUser('afpy_test_user')
        assert user is not None

        mail = self.mail_output()
        mail.mustcontain('afpy_test_user', user.street[0:6])

        response = self.app.get(url(controller='register', action='confirm', uid=user.uid, key=user.street))
        assert 'Votre+inscription+est+maintenant' in response.location, response


    def tearDown(self):
        user = ldap.getUser('afpy_test_user')
        if user is not None:
            user.conn.delete(user)

