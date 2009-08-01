from members.tests import *
from afpy.ldap import custom as ldap

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
                                dict(letter='pasgrimaud'),
                                extra_environ=admin_environ)
        resp.mustcontain('gawel', 'infos', '+')


    def test_subscribe_payed(self):
        resp = self.app.post(url(controller='my', action='subscribe'),
                             dict(paymentComment='my comment',
                                  paymentObject=ldap.PERSONNAL_MEMBERSHIP,
                                  paymentMode='payed'),
                              extra_environ=admin_environ)

        resp.mustcontain("Un courriel vous a")

        mail = self.mail_output()
        mail.mustcontain("- Mode de paiement: payed", 'my comment')

    def test_subscribe_cheque(self):
        resp = self.app.post(url(controller='my', action='subscribe'),
                             dict(paymentComment='my comment',
                                  paymentObject=ldap.PERSONNAL_MEMBERSHIP,
                                  paymentMode='cheque'),
                              extra_environ=admin_environ)

        resp.mustcontain("vous devez maintenant nous faire parvenir", "Tresorier de l'association")

        mail = self.mail_output()
        mail.mustcontain("- Mode de paiement: cheque", 'my comment')

    def test_subscribe_paypal(self):
        resp = self.app.post(url(controller='my', action='subscribe'),
                             dict(paymentComment='my comment',
                                  paymentObject=ldap.PERSONNAL_MEMBERSHIP,
                                  paymentMode='paypal'),
                              extra_environ=admin_environ)

        resp.mustcontain('https://www.paypal.com/fr/cgi-bin/webscr')

        mail = self.mail_output()
        mail.mustcontain("- Mode de paiement: paypal")
