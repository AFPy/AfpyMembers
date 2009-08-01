# -*- coding: utf-8 -*-
from members.forms import *
from formalchemy.fields import SelectFieldRenderer, IntegerFieldRenderer
from members.forms import FieldSet as BaseFieldSet
__doc__ = '''
>>> from afpy.ldap import custom as ldap
>>> payments = ldap.getUser('gawel').payments
>>> form = PaymentForm.bind(payments[0])
>>> form.paymentDate.render()
'2005-01-01'
>>> form.paymentAmount.value
20
>>> print form.paymentAmount.render()
<input id="Payment-20050101000000Z-paymentAmount" name="Payment-20050101000000Z-paymentAmount" size="5" type="text" value="20" />

>>> form = NewPaymentForm.bind(ldap.Payment())
>>> print form.paymentDate.render() #doctest: +ELLIPSIS
<span id="Payment--paymentDate">...

'''

class ObjectRenderer(SelectFieldRenderer):
    def render(self, **kwargs):
        options = [(v.decode('utf-8'), k) \
                        for k, v in sorted(ldap.PAYMENTS_OPTIONS.items())]
        return super(ObjectRenderer, self).render(options=options, **kwargs)
    def render_readonly(self):
        return ldap.PAYMENTS_OPTIONS.get(self._value)

class IntRenderer(IntegerFieldRenderer):
    def render(self, **kwargs):
        kwargs['size'] = '5'
        return IntegerFieldRenderer.render(self, **kwargs)

template_header = r"""
<tr>
% for field in fieldset.render_fields.itervalues():
<th ${'paymentAmount' not in field.name and 'width="150"' or ''}>
${field.label_text}
</th>
% endfor
%if not fieldset.readonly:
<th>Actions</th>
%endif
</tr>
""".strip()

template_render = r"""
<table width="100%" class="payments_listing listing">
<tr>
% for field in fieldset.render_fields.itervalues():
<td ${'paymentAmount' not in field.name and 'width="150"' or ''}
    align="center">
    %if field.is_readonly():
        ${field.render_readonly()}
        <div style="display:none">
        ${field.render()}
        </div>
    %else:
        ${field.render()}
    %endif
</td>
% endfor
<td>
%if fieldset.model._pk:
<div>
<input type="hidden" name="dn" value="${fieldset.model._dn}" />
${h.link_to_function('Sauver', h.remote_function(
        url=h.url_for(action='edit'),
        submit=fieldset.model._pk,
        update='payments_%s' % user.uid))}
</div>
<div>
${h.link_to_function('Supprimer', h.remote_function(
        url=h.url_for(action='delete'),
        submit=fieldset.model._pk,
        update='payments_%s' % user.uid))}
<div>
%else:
<input type="submit" class="context" value="Ajouter" />
%endif
</td>
</tr>
</table>
""".strip()

template_render_readonly = r"""
<tr>
% for field in fieldset.render_fields.itervalues():
%if 'uid' not in field.name:
<td width="20%">${field.render_readonly()}</td>
%endif
% endfor
</tr>
""".strip()

class FieldSet(BaseFieldSet):
    _render_header = staticmethod(Template(template_header).render_unicode)
    _render = staticmethod(Template(template_render).render)
    _render_readonly = staticmethod(Template(template_render_readonly).render_unicode)

    def header(self):
        return self._render_header(fieldset=self)

PaymentForm = FieldSet(ldap.Payment)
PaymentForm.configure(include=[PaymentForm.paymentDate.readonly(), PaymentForm.paymentObject.with_renderer(ObjectRenderer),
                      PaymentForm.paymentAmount.with_renderer(IntRenderer), PaymentForm.invoiceReference])

NewPaymentForm = FieldSet(ldap.Payment)
NewPaymentForm.configure(include=[NewPaymentForm.paymentDate, NewPaymentForm.paymentObject.with_renderer(ObjectRenderer),
                      NewPaymentForm.paymentAmount.with_renderer(IntRenderer), NewPaymentForm.invoiceReference])

