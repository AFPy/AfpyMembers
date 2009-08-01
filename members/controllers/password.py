# -*- coding: utf-8 -*-
import logging

from members.lib.base import *
from webhelpers.rails.tags import content_tag
from afpy.mail import LDAPMailTemplate
import md5, random, string

log = logging.getLogger(__name__)

tag = content_tag


class PasswordController(BaseController):

    def index(self):
        return render('/password.mako')

    def password_form(self,uid='',mail='',errors=''):
        element = 'password_form'
        errors = display_errors(errors)
        description = h.content_tag('p', u"""Saisissez votre login ou votre
                                         courriel puis validez pour réinitialiser
                                         votre mot de passe""",
                                         **{'class':'documentDescription'})
        form = ''
        for name, value in (('uid',uid),('mail',mail)):
            form += ldap_field(name, value)
        form += h.content_tag('td',
                h.submit('Valider', name='validate', **{'class':'context'}),
                colspan="2", align='center')
        form = tag('table', form)
        return h.form_remote_tag(
                    url=h.url_for(action='change_password', id=None),
                    update=dict(success=element, failure=element)
                    ) + errors + description + form + h.end_form()

    def change_password(self):
        uid = request.POST.get('uid')
        mail = request.POST.get('mail')

        user = None
        errors = []
        passwd = ''.join(random.sample(string.ascii_letters,6))

        if uid:
            if ldap.isUser(uid):
                user = ldap.User(uid)
            else:
                errors.append('Impossible de trouver votre login')

        if not user and mail:
            members = ldap.conn.search(ldap.conn.members_dn,filter='(mail=%s)' % mail)
            if len(members) == 1:
                dn = members[0][0]
                dn = ldap.getDN(dn)
                user = ldap.User(dn)
            else:
                errors.append('Impossible de trouver votre courriel')

        if user:
            ldap.changePassword(user.uid, passwd)
            manage_ZopeUser('edit', str(user.uid), passwd)

            mail = LDAPMailTemplate(name='send_password',
                                    subject='Votre mot de passe sur afpy.org',
                                    passwd=passwd,
                                    mfrom='postmaster@afpy.org')
            mail.send(user.uid)
            return u"""Votre mot de passe à été modifié. Vous allez recevoir un
                    courriel de confirmation."""

        errors.insert(0,'Impossible de vous identifier')
        return self.password_form(uid=uid, mail=mail, errors=errors)


