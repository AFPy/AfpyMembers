from members.tests import *

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


