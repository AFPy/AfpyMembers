import logging

from repoze.what import predicates
from repoze.what.plugins.pylonshq import ActionProtector
from repoze.what.plugins.pylonshq import ControllerProtector


from members.lib.base import *
from members.forms.payments import NewPaymentForm, PaymentForm
from datetime import datetime
from datetime import timedelta

log = logging.getLogger(__name__)

def payment_dn(fs, id):
    dn = ldap.getDN(id)
    dn = 'paymentDate=%s,%s' % (fs.uid.value, dn)
    return dn

class PaymentsController(BaseController):

    def index(self):
        payments = self.user.payments
        c.forms = []
        for payment in payments:
            fs = PaymentForm.bind(payment)
            fs.readonly = True
            c.forms.append(fs)
        c.user = self.user
        return render('/payments.mako')

    @ActionProtector(predicates.in_group('bureau'))
    def edit(self, id, message=None):
        id = str(id)
        c.user = ldap.getUser(id)
        dn = request.POST.get('dn')

        # forms
        payments = c.user.payments
        c.forms = []
        for payment in payments:
            if request.POST and payment._dn == dn:
                fs = PaymentForm.bind(payment, data=request.POST or None)
                if fs.validate():
                    fs.sync()
                    payment.save()
                    ldap.updateExpirationDate(user)
            fs = PaymentForm.bind(payment)
            c.forms.append(fs)

        # add form
        now = datetime.now()
        new_date = now
        payments = [p for p in payments if p.paymentAmount]
        if payments:
            last_payment = payments[-1]
            d = h.to_python(h.to_string(last_payment.paymentDate), datetime)
            if d + timedelta(365) < now - timedelta(90):
                new_date = d + timedelta(365)
        payment = ldap.Payment()
        payment.paymentDate = new_date
        payment.paymentObject = ldap.PERSONNAL_MEMBERSHIP
        c.new = NewPaymentForm.bind(payment, request.POST or None)
        c.message = message
        return render('/edit_payments.mako')

    @ActionProtector(predicates.in_group('bureau'))
    def delete(self, id):
        user = ldap.getUser(id)
        dn = request.POST['dn']
        for p in user.payments:
            if p._dn == dn:
                user._conn.delete(p)
                ldap.updateExpirationDate(user)
                break
        ldap.updateExpirationDate(user)
        message = 'Supprimer a %s' % datetime.now().strftime('%H:%M:%S')
        return self.edit(id, message=message)

    @ActionProtector(predicates.in_group('bureau'))
    def add(self, id):
        id = str(id)
        payment = ldap.Payment()
        fs = NewPaymentForm.bind(payment, data=request.POST)
        if fs.validate():
            fs.sync()
            user = ldap.getUser(id)
            user.append(payment)
            payment.save()
            message = 'Ajouter a %s' % datetime.now().strftime('%H:%M:%S')
        else:
            message = 'Erreur a %s' % datetime.now().strftime('%H:%M:%S')
        return self.edit(id, message=message)


PaymentsController = ControllerProtector(predicates.not_anonymous())(PaymentsController)
