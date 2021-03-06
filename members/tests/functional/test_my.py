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


    def test_subscribe_payed(self):
        resp = self.app.post(url(controller='my', action='subscribe'),
                             dict(paymentComment='my comment payed',
                                  paymentObject=ldap.PERSONNAL_MEMBERSHIP,
                                  paymentDate='20000101000000Z',
                                  paymentMode='payed'),
                              extra_environ=admin_environ)

        resp.mustcontain("Un courriel vous a")

        mail = self.mail_output()
        mail.mustcontain("- Mode de paiement: payed", 'my comment')

        u = ldap.getUser('gawel')
        assert 'payed' in u.payments[0].invoiceReference

    def test_subscribe_cheque(self):
        resp = self.app.post(url(controller='my', action='subscribe'),
                             dict(paymentComment='my comment cheque',
                                  paymentObject=ldap.PERSONNAL_MEMBERSHIP,
                                  paymentDate='20000101000000Z',
                                  paymentMode='cheque'),
                              extra_environ=admin_environ)

        resp.mustcontain("vous devez maintenant nous faire parvenir", "Tresorier de l'association")

        mail = self.mail_output()
        mail.mustcontain("- Mode de paiement: cheque", 'my comment')

        u = ldap.getUser('gawel')
        assert 'cheque' in u.payments[0].invoiceReference

    def test_subscribe_paypal(self):
        resp = self.app.post(url(controller='my', action='subscribe'),
                             dict(paymentComment='my comment paypal',
                                  paymentObject=ldap.PERSONNAL_MEMBERSHIP,
                                  paymentDate='20000101000000Z',
                                  paymentMode='paypal'),
                              extra_environ=admin_environ)

        resp.mustcontain('https://www.paypal.com/fr/cgi-bin/webscr')

        mail = self.mail_output()
        mail.mustcontain("- Mode de paiement: paypal")

        u = ldap.getUser('gawel')
        assert 'paypal' in u.payments[0].invoiceReference

    def test_change_password(self):
        resp = self.app.post(url(controller='my', action='change_password'),
                             dict(passwd='old_password',
                                  new_passwd='new_passwd',
                                  confirm_passwd='new_passwd',
                                  ),
                              extra_environ=admin_environ)

        resp.mustcontain('http://www.afpy.org/?portal_status_message=Mot')

        mail = self.mail_output()
        mail.mustcontain("Nom d'utilisateur: gawel",
                         "Mot de passe: new_passwd")



    def tearDown(self):
        TestController.tearDown(self)
        u = ldap.getUser('gawel')
        p = u.payments[0]
        if p.get('paymentDate') == '20000101000000Z':
            p.conn.delete(p)

