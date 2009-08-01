import logging

from repoze.what import predicates
from repoze.what.plugins.pylonshq import ActionProtector
from repoze.what.plugins.pylonshq import ControllerProtector

from members.lib.base import *
from members.forms.users import NewUserForm
from members.forms.payments import NewPaymentForm, PaymentForm
from afpy.mail import LDAPMailTemplate
from afpy.core import mailman
import random, string
import datetime

log = logging.getLogger(__name__)

class AdminController(BaseController):

    def index(self):
        return ''

    def new(self):
        message = ''
        user = ldap.AfpyUser()
        user.st = 'FR'
        fs = NewUserForm.bind(user, data=request.POST or None)

        payment = ldap.Payment()
        payment.paymentDate = h.to_python(h.to_string(datetime.datetime.now()), datetime.date)
        payment.paymentObject = ldap.PERSONNAL_MEMBERSHIP
        fs2 = NewPaymentForm.bind(payment, data=request.POST or None)

        if request.POST:
            if fs.validate() and fs2.validate():
                fs.sync()
                fs2.sync()

                uid = fs.uid.value
                conn = ldap.get_conn()

                user._dn = conn.uid2dn(uid)
                user.cn = user.uid
                conn.add(user)
                user.append(payment)


                # add user
                passwd = ''.join(random.sample(string.ascii_letters,6))
                user.change_password(passwd)
                manage_ZopeUser('add', uid, passwd)

                # ml
                mailman.subscribeTo('afpy-membres', user)

                # confirmation
                mail = LDAPMailTemplate(
                        name='new_members',
                        subject='Votre inscription sur afpy.org',
                        signature='tresorier',
                        passwd=passwd,
                        member=user,
                        mfrom='noreply@afpy.org', **data)

                if '/test_' in request.environ['SCRIPT_NAME']:
                    mail.send(user, cc='www@afpy.org')
                else:
                    mail.send(user, cc='tresorerie@afpy.org')

                # result in readonly
                fs = NewUserForm.bind(user)
                fs2 = NewPaymentForm.bind(payment)
                fs.readonly = True
                fs2.readonly = True

                message = 'Utilisateur ajout&eacute; et son mot de passe envoy&eacute; par courriel'

        c.title = 'Inscription de membre'
        html = h.form(h.url_for())
        html += fs.render(message=message)
        if fs2.readonly:
            html += '<table width="100%" class="payments_listing listing">'
            html += fs2.header()
            html += fs2.render()
            html += '</table>'
        else:
            html += '<table width="100%" class="payments_listing listing">'
            html += fs2.header()
            html += '</table>'
            html += fs2.render()
        html += h.end_form()
        c.body = html
        return render('/generic.mako')

AdminController = ControllerProtector(predicates.in_group('bureau'))(AdminController)

