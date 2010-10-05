# -*- coding: utf-8 -*-
from members.forms import *
from formalchemy import Field
from formalchemy.fields import SelectFieldRenderer, PasswordFieldRenderer
from afpy.core.countries import COUNTRIES

class CountriesRenderer(SelectFieldRenderer):
    def render(self, **kwargs):
        options = [(v.decode('utf-8'), k) for k, v in sorted(COUNTRIES.items())]
        return super(CountriesRenderer, self).render(options=options, **kwargs)
    def render_readonly(self):
        return COUNTRIES.get(self._value)

class RoleRenderer(SelectFieldRenderer):
    def render(self, **kwargs):
        options = ['', 'president', 'vice-president', 'tresorier', 'vice-tresorier', 'secretaire', 'vice-secretaire']
        options = [(v, v) for v in options]
        return super(RoleRenderer, self).render(options=options, **kwargs)


__doc__ = '''
>>> from afpy.ldap import custom as ldap
>>> user = ldap.getUser('gawel')
>>> user.uid
'gawel'
>>> form = UserForm.bind(user)
>>> form.uid.value
'gawel'
>>> print form.uid.render()
<input id="User-gawel-uid" name="User-gawel-uid" type="hidden" value="gawel" />

'''

UserForm = FieldSet(ldap.User)
UserForm.configure(include=[UserForm.uid.hidden(), UserForm.sn,
                      UserForm.mail.validate(validators.email),
                      UserForm.telephoneNumber, UserForm.birthDate,
                      UserForm.street, UserForm.postalCode, UserForm.l, UserForm.st.with_renderer(CountriesRenderer)])

AdminUserForm = FieldSet(ldap.User)
AdminUserForm.configure(include=[AdminUserForm.uid.hidden(), AdminUserForm.sn, AdminUserForm.title.with_renderer(RoleRenderer),
                                AdminUserForm.mail.validate(validators.email),
                          AdminUserForm.emailAlias, AdminUserForm.labeledURI,
                          AdminUserForm.telephoneNumber, AdminUserForm.birthDate,
                          AdminUserForm.street, AdminUserForm.postalCode, AdminUserForm.l, AdminUserForm.st.with_renderer(CountriesRenderer)])

NewUserForm = FieldSet(ldap.User)
NewUserForm.configure(include=[NewUserForm.uid.validate(validate_uid),
                          NewUserForm.sn, NewUserForm.mail.validate(validate_email),
                          NewUserForm.telephoneNumber, NewUserForm.birthDate,
                          NewUserForm.street, NewUserForm.postalCode, NewUserForm.l, NewUserForm.st.with_renderer(CountriesRenderer)])

RegisterForm = FieldSet(ldap.User)
RegisterForm.append(Field('password'))
RegisterForm.configure(include=[RegisterForm.uid.validate(validate_uid),
                                RegisterForm.sn, RegisterForm.mail.validate(validate_email),
                                RegisterForm.password.label('Mot de passe').with_renderer(
                                              PasswordFieldRenderer).required()])

