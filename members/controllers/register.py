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
        form = RegisterForm.bind(ldap.AfpyUser(), data=request.POST)

        if form.validate():
            uid = str(form.uid.value)
            sn = form.sn.value
            mail = str(form.mail.value)
            passwd = str(form.password.value)
            key = md5.new(''.join(
                    random.sample(string.ascii_letters,6))).hexdigest()
            conn = ldap.get_conn()
            user = ldap.AfpyUser(uid=uid, conn=conn,
                                 attrs=dict(sn=sn, mail=mail,
                                 street=key, st='UNCONFIRMED'))
            conn.save(user)
            user.change_password(passwd)
            manage_ZopeUser('add', uid, passwd)

            confirm_url = 'http://www.afpy.org' + h.url_for(
                                    action='confirm',
                                    uid=uid,
                                    key=key)
            mail = LDAPMailTemplate(
                        name='send_key',
                        subject='Votre inscription sur afpy.org',
                        confirm_url=confirm_url, passwd=passwd,
                        mfrom='noreply@afpy.org')
            mail.send(uid)
            return u"""Votre inscription a été prise en compte. Vous allez
                    recevoir un courriel de confirmation."""
        return self.register_form(fs=form)

    def confirm(self, uid, key):
        user = ldap.getUser(uid)
        if user:
            url = 'http://www.afpy.org/membres/login?portal_status_message='
            url += 'Votre inscription est maintenant confirmée'
            if str(user.street) == str(key):
                user.street=' '
                user.st='FR'
                user.save()
                redirect_to(url)
        return 'You lose'


