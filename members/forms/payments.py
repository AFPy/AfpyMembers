# -*- coding: utf-8 -*-
from members.forms import *
from mako.template import Template
from formalchemy.fields import SelectFieldRenderer, IntegerFieldRenderer
from members.forms import FieldSet as BaseFieldSet
from members.forms import TemplateEngine as BaseTemplateEngine
__doc__ = '''
>>> from afpy.ldap import custom as ldap
>>> payments = ldap.getUser('gawel').payments
>>> payment = payments[0]
>>> getattr(payment, 'paymentDate')
datetime.date(2005, 1, 1)
>>> form = PaymentForm.bind(payment)
>>> form.paymentDate.render()
'2005-01-01'
>>> form.paymentAmount.value
20
>>> print form.paymentAmount.render()
<input id="Payment-20050101000000z-paymentAmount" name="Payment-20050101000000z-paymentAmount" size="5" type="text" value="20" />

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

class TemplateEngine(BaseTemplateEngine):
    prefix = 'payment'

class FieldSet(BaseFieldSet):
    _render_header = staticmethod(Template(template_header).render_unicode)
    engine = TemplateEngine()

    def header(self):
        return self._render_header(fieldset=self)

PaymentForm = FieldSet(ldap.Payment)
PaymentForm.configure(include=[PaymentForm.paymentDate.readonly(), PaymentForm.paymentObject.with_renderer(ObjectRenderer),
                      PaymentForm.paymentAmount.with_renderer(IntRenderer), PaymentForm.invoiceReference])

NewPaymentForm = FieldSet(ldap.Payment)
NewPaymentForm.configure(include=[NewPaymentForm.paymentDate, NewPaymentForm.paymentObject.with_renderer(ObjectRenderer),
                      NewPaymentForm.paymentAmount.with_renderer(IntRenderer), NewPaymentForm.invoiceReference])

