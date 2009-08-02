import logging
import os

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

    def letters(self, id='all'):
        """ letters menu """
        stype = id
        for label,v in h.MEMBER_TYPES:
            if stype == v:
                break
        if v == 'search':
            form = h.form_remote_tag(
                   url=h.url(controller='admin', action='subscribers',
                                 stype='search', letter='all'),
                   update=dict(success='contents', failure='contents'))
            contents = form + h.text_field('letter') + \
                       h.submit('Rechercher') + h.end_form()
        else:
            menus = [(l.upper(), h.url(controller='admin', action='subscribers',
                                       stype=stype,letter=l)) \
                    for l in string.ascii_lowercase]
            contents = h.get_menu(menus, tag='div', stag='span')
        return tag('h1', label) + tag('fieldset',
                                      tag('legend', 'Navigation') + \
                   contents)

    def subscribers(self, stype='', letter=''):
        """ get subscribers listing """
        if stype == 'members':
            f = '(&(!(membershipExpirationDate=*))(uid=%s*))' % letter
        elif stype == 'subscribers':
            f = '(&(membershipExpirationDate=*)(uid=%s*))' % letter
        elif stype == 'search':
            letter = request.POST['letter']
            f = '(&(objectClass=person)(sn=*%s*))' % letter
        else:
            f = '(&(objectClass=person)(uid=%s*))' % letter
        conn = ldap.get_conn()
        res = conn.search_nodes(filter=f, attrs=['uid'])
        members = [m.uid for m in res]
        members.sort()
        c.members = members
        return render('/listing.mako')

    def awaiting(self):
        c.listing_title = 'Payments en attente'
        c.members = ldap.getAwaitingPayments()
        return render('/listing.mako')

    def new(self):
        message = ''
        user = ldap.AfpyUser()
        user.l = 'Paris'
        user.st = 'FR'
        fs = NewUserForm.bind(user, data=request.POST or None)

        payment = ldap.Payment()
        payment.paymentDate = h.to_python(h.to_string(datetime.datetime.now()), datetime.date)
        payment.paymentObject = ldap.PERSONNAL_MEMBERSHIP
        payment.paymentAmount = 20
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

                if not h.DEV_MOD:
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

                    mail.send(user, cc='tresorerie@afpy.org')

                # result in readonly
                fs = NewUserForm.bind(user)
                fs2 = NewPaymentForm.bind(payment)
                fs.readonly = True
                fs2.readonly = True

                message = 'Utilisateur ajout&eacute; et son mot de passe envoy&eacute; par courriel'

        c.title = 'Inscription de membre'
        html = h.form(h.url_for(id=None), id="new_user")
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
        return str(render('/generic.mako'))

AdminController = ControllerProtector(predicates.in_group('bureau'))(AdminController)

