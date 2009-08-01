# -*- coding: utf-8 -*-
import logging

from members.lib.base import *
from members.forms.users import RegisterForm
from afpy.mail import LDAPMailTemplate
import md5, random, string

log = logging.getLogger(__name__)


class RegisterController(BaseController):

    def index(self):
        return render('/register.mako')

    def register_form(self, fs = None):
        element = 'register_form'
        if not fs:
            fs = RegisterForm.bind(ldap.AfpyUser())
        form = fs.render()
        form += h.submit('Valider', name='validate', **{'class':'context'})
        return '\n'.join([
                    '<div>',
                    h.form_remote_tag(
                        url=h.url_for(action='register',id=None),
                        update=dict(success=element, failure=element)
                        ),
                    form,
                    h.end_form(),
                    '</div>'])

    def register(self):
        conn = ldap.get_conn()
        user = ldap.AfpyUser()
        form = RegisterForm.bind(user, data=request.POST)

        if form.validate():
            form.sync()
            passwd = str(form.password.value)
            delattr(user, 'password')
            key = md5.new(''.join(
                    random.sample(string.ascii_letters,6))).hexdigest()
            user.cn = user.uid
            user.uid = user.uid.lower()
            user.st = 'UNCONFIRMED'
            user.street = key
            user._dn = conn.uid2dn(user.uid)
            conn.add(user)
            user.change_password(str(form.password.value))

            if not h.DEV_MOD:
                manage_ZopeUser('add', uid, passwd)

            confirm_url = 'http://www.afpy.org' + h.url_for(
                                    action='confirm',
                                    uid=user.uid,
                                    key=key)
            mail = LDAPMailTemplate(
                        name='send_key',
                        subject='Votre inscription sur afpy.org',
                        confirm_url=confirm_url, passwd=passwd,
                        mfrom='noreply@afpy.org')
            mail.send(user)
            return u"""Votre inscription a été prise en compte. Vous allez
                    recevoir un courriel de confirmation."""
        return self.register_form(fs=form)

    def confirm(self, uid, key):
        user = ldap.getUser(uid)
        if user:
            url = h.url(controller='utils', action='login',
                        portal_status_message='Votre inscription est maintenant confirmée')
            if str(user.street) == str(key):
                user.street=' '
                user.st='FR'
                user.save()
                redirect_to(url)
        return 'You lose'


