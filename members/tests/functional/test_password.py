from members.tests import *
from afpy.ldap import custom as ldap

class TestPasswordController(TestController):

    def setUp(self):
        TestController.setUp(self)
        self.user = ldap.AfpyUser()
        self.user.uid = 'afpy_test_user'
        self.user.cn = 'afpy_test_user'
        self.user.sn = 'afpy_test_user'
        self.user.mail = 'afpy_test_user@afpy.org'
        self.user.dn
        self.conn = ldap.get_conn()
        self.conn.add(self.user)

    def test_change_fail(self):
        resp = self.app.post(url(controller='password', action='change_password'),
                            dict(uid='afpy_test_user_afpy_test_user')
                            )
        resp.mustcontain('Impossible de vous identifier',
                         'Saisissez votre login ou votre')
        resp = self.app.post(url(controller='password', action='change_password'),
                            dict(mail='afpy_test_user_afpy_test_user@afpy.org')
                            )
        resp.mustcontain('Impossible de vous identifier',
                         'Saisissez votre login ou votre')

    def test_change_by_uid(self):
        resp = self.app.post(url(controller='password', action='change_password'),
                            dict(uid='afpy_test_user')
                            )
        resp.mustcontain('Votre mot de passe')

        mail = self.mail_output()
        mail.mustcontain("Nom d'utilisateur: afpy_test_user",
                         "Mot de passe:")

    def test_change_by_email(self):
        resp = self.app.post(url(controller='password', action='change_password'),
                            dict(mail='afpy_test_user@afpy.org')
                            )
        resp.mustcontain('Votre mot de passe')

        mail = self.mail_output()
        mail.mustcontain("Nom d'utilisateur: afpy_test_user",
                         "Mot de passe:")

    def tearDown(self):
        TestController.tearDown(self)
        self.conn.delete(self.user)
