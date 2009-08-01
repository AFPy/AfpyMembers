# -*- coding: utf-8 -*-
from mako.template import Template
from formalchemy import SimpleMultiDict
from formalchemy import validators
from formalchemy import ValidationError
from formalchemy import types
from formalchemy import config
from afpy.ldap import custom as ldap
from afpy.ldap.forms import FieldSet as BaseFieldSet, Grid as BaseGrid, Field
from datetime import timedelta
from datetime import datetime
from datetime import date
import string

class TestRequest(object):
    POST = None

template_render = r"""
<%
_ = F_
_focus_rendered = False
%>\

% for error in fieldset.errors.get(None, []):
<div class="portalMessage">
  ${_(error)}
</div>
% endfor

% for field in fieldset.render_fields.itervalues():
  % if field.requires_label:
<div class="field">
  <label for="${field.renderer.name}">${field.label_text or fieldset.prettify(field.key)}</label>
  %if field.is_required():
      <span class="field_req">*</span>
  %endif
  <div></div>
  ${field.render()}
  <div class="formHelp">
  % for error in field.errors:
  <span class="field_error">${_(error)}</span>
  % endfor
  </div>
</div>

% if (fieldset.focus == field or fieldset.focus is True) and not _focus_rendered:
<script type="text/javascript">
//<![CDATA[
document.getElementById("${field.renderer.name}").focus();
//]]>
</script>
<% _focus_rendered = True %>\
% endif
  % else:
${field.render()}
  % endif
% endfor
""".strip()

template_render_readonly = r"""
%if message:
    <div class="portalMessage">
    ${message}
    </div>
%endif
% for field in fieldset.render_fields.itervalues():
<div class="field">
  <label>${field.label_text or fieldset.prettify(field.key)}</label>
  : ${field.render_readonly()}
<div>
%endfor
"""
class FieldSet(BaseFieldSet):

    _render = staticmethod(Template(template_render).render_unicode)
    _render_readonly = staticmethod(Template(template_render_readonly).render_unicode)

def validate_uid(value):
    try:
        value = str(value)
    except UnicodeEncodeError:
        raise validators.ValidationError(
                "Le login ne doit contenir que de l'ASCII")
    for v in value:
        if v not in string.ascii_letters+'_.':
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

def validate_email(value):
    validators.email(value)
    conn = ldap.get_conn()
    if conn.search(filter='(mail=%s)' % value):
        raise validators.ValidationError('Cet email est pris')
    return value

