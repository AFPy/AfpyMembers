# -*- coding: utf-8 -*-
from formalchemy import SimpleMultiDict
from formalchemy import validators
from formalchemy import ValidationError
from formalchemy import types
from formalchemy import templates
from formalchemy import config as fa_config
from webhelpers.html import literal
from afpy.ldap import custom as ldap
from afpy.ldap.forms import FieldSet as BaseFieldSet, Grid as BaseGrid, Field
from members.lib.base import render
from datetime import timedelta
from datetime import datetime
from datetime import date
import string

class TestRequest(object):
    POST = None

fa_config.encoding = 'utf-8'

class TemplateEngine(templates.TemplateEngine):
    prefix = 'fieldset'
    def render(self, name, **kwargs):
        if 'readonly' in name:
            name = '%s_readonly' % self.prefix
        else:
            name = self.prefix
        return literal(render('/forms/%s.mako' % name, extra_vars=kwargs))
fa_config.engine = TemplateEngine()

class FieldSet(BaseFieldSet):
    engine = TemplateEngine()

def validate_uid(value, field):
    try:
        value = str(value)
    except UnicodeEncodeError:
        raise validators.ValidationError(
                "Le login ne doit contenir que de l'ASCII")
    for v in value:
        if v not in string.ascii_letters+'-_':
            raise validators.ValidationError(
                "Le login ne doit contenir que de l'ASCII")
    if ' ' in value:
        raise validators.ValidationError(
                "Le login ne doit pas contenir d'espace")
    if len(value) < 4:
        raise validators.ValidationError(
                "Le login doit contenir au moins 4 characteres")
    if ldap.getUser(value):
        raise validators.ValidationError('Cet identifiant est pris')
    return value

def validate_email(value, field):
    validators.email(value)
    conn = ldap.get_conn()
    if conn.search(filter='(mail=%s)' % value):
        raise validators.ValidationError('Cet email est pris')
    return value

