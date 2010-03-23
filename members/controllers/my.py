# -*- coding: utf-8 -*-
import datetime
import logging

from repoze.what import predicates
from repoze.what.plugins.pylonshq import ActionProtector
from repoze.what.plugins.pylonshq import ControllerProtector

from members.lib.base import *
from members.forms.users import UserForm, AdminUserForm
from members.forms import ValidationError
from webhelpers.html.tags import *
from afpy.core import mailman
from afpy.mail import LDAPMailTemplate
from afpy.ldap import custom as ldap
import string, datetime

log = logging.getLogger(__name__)

def tag(name, *args, **kwargs):
    return h.HTML.tag(name, *args, **kwargs)

def form_message(message):
    return u'%s - %s' % (message, datetime.datetime.now().strftime('%H:%M:%S'))

class MyController(BaseController):

    def index(self):
        c.user_id = self.user.uid
        return render('/site.mako')

    def courrier(self):
        c.u = AdminUserForm.bind(self.user)
        u = ldap.getUserByTitle('tresorier')
        c.fs = AdminUserForm.bind(u)
        c.now = datetime.datetime.now()
        response.headers['x-deliverance-no-theme'] = 'true'
        request.environ['afpy.skin.none'] = True
        return render('/courrier.mako')

    def bulletin(self):
        u = ldap.getUserByTitle('tresorier')
        c.fs = AdminUserForm.bind(u)
        c.fs.readonly = True
        c.now = datetime.datetime.now()
        response.headers['x-deliverance-no-theme'] = 'true'
        request.environ['afpy.skin.none'] = True
        return render('/bulletin.mako')

    def menu(self):
        """ left menu """
        user = self.user_id
        menus = ((u'Mes informations',h.url(controller='my', action='info')),
                 ('Mes Listes', h.url(controller='my', action='listes')),
                 ('Mes paiements', h.url('payments', id=user)),
                 ('Mon mot de passe', h.url(controller='my', action='password_form')))

        if self.user.expired:
            menus = ((h.literal(u"<span style='color:red'>Adhérer à l'afpy</span>"),
                      h.url('adhesion', no_remote='true')),) + menus
        html = h.get_menu(menus, empty='letters')

        if self.admin:
            user += ' (Admin)'
            menus = [(l, h.url(controller='admin', action='letters', id=v)) for l,v in h.MEMBER_TYPES]
            html += h.get_menu(menus, element='letters', empty='contents')

            menus = [(l, h.url(controller='admin', action=v)) for l,v in [('Payments en attente', 'awaiting')]]
            html += h.get_menu(menus, element='contents', empty='letters')

            menus = (
                     (u"Inscription manuelle",
                      h.url(controller='admin', action='new',
                                no_remote='true')),
                     (u"Impression bulletin",
                      h.url(controller='my', action='bulletin',
                                no_remote='true', notheme='true')),
                    )
            html += h.get_menu(menus)

        # plone presentation...
        html = str(html).replace('dl>','div>')
        html = html.replace('<dd>','<div class="nav1">')
        html = html.replace('</dd>','</div>')
        return h.literal("""
        <div class="portlet">
            <h5>Espace de %s</h5>
            <div class="portletBody">
            %s
            </div>
        </div><div>&nbsp;</div>
        """) % (user, h.literal(html))

    def info(self, id=None):
        """ user form """
        admin = self.admin
        if admin and id:
            user = ldap.getUser(id)
        else:
            user = self.user

        if user != self.user and not admin:
            raise NotAuthorizedError()

        html = title = ''
        if admin:
            fs_klass = AdminUserForm
            fs = AdminUserForm
        else:
            fs_klass = UserForm

        fs = fs_klass.bind(user, data=request.POST or None)

        if request.POST and fs.validate():
            fs.sync()
            user.save()
            fs = fs_klass.bind(user, data=None)
            message = form_message(u'Modifie').encode('utf-8')
            e = ValidationError(message)
            fs._errors = [e]

        html += fs.render()

        if admin and id:
            element = 'infos_%s' % user.uid
            url = h.url(controller='my', action='info',id=id)
        else:
            element = 'contents'
            url = h.url(controller='my', action='info')
        form = h.form(url=url, class_="remote", onsubmit="return remote_form(this);", alt=element)
        html = title + tag('fieldset', h.literal(tag('legend', u'Mes informations')) + \
                h.literal(form) + h.literal(tag('table', h.literal(html))) + \
                h.submit("save", "Sauver", class_='context') + h.literal('</form>'))
        return html

    def listes(self, id='', errors=''):
        user = id and ldap.getUser(id) or self.user
        admin = self.admin

        html = title = ''
        if user != self.user and not admin:
            raise NotAuthorizedError()

        if admin and self.user != user:
            element = 'listes_%s' % user
            hidden = h.hidden_field('uid',user.uid)
        else:
            element = 'contents'
            hidden = ''
        html += tag('legend', 'Listes de diffusion')
        html += display_errors(errors)
        html += h.form(url=h.url.current(action='save_listes',id=None),
                       class_='remote', onsubmit="return remote_form(this);", alt=element)
        html += hidden

        email = user.email
        selected = mailman.lists.getListsFor(email)
        for ml in mailman.lists.values():
            # hide private list if not subbcribed
            if ml.name == 'afpy-membres' and getattr(user, 'membershipExpirationDate', None):
                pass
            elif not admin and not ml.public and ml.name not in selected:
                continue
            html += h.literal('<div>')
            html += h.checkbox('selected',
                                id=ml.name,
                                checked=ml.name in selected,
                                value=ml.name)
            html += h.literal(' ')
            html += tag('label', ml.title, **{'for':ml.name})
            html += h.literal(' (')
            html += h.link_to('infos',
                         'http://lists.afpy.org/mailman/listinfo/%s' % ml.name)
            html += h.literal(')')
            html += h.literal('</div>')

        html += tag('div', h.literal('&nbsp;'))
        html += h.submit('save', 'Sauver', **{'class':'context'})
        html += h.end_form()

        return tag('fieldset', html)

    def save_listes(self):
        """ save mailing lists
        """
        user = self.user_id
        admin = self.admin
        uid = request.POST.get('uid')
        if admin and uid:
            user = ldap.getUser(uid)
        else:
            user = self.user
        email = user.email
        new_selected = request.POST.getall('selected')
        selected = mailman.lists.getListsFor(email)
        for ml in mailman.lists.values():
            if ml.name in new_selected:
                if ml.name not in selected:
                    if ml.name == 'afpy-membres' and user.expired:
                        continue
                    elif not self.admin and not ml.public:
                        continue
                    else:
                        ml.append(email)
            elif ml.name in selected:
                del ml[email]
        return self.listes(id=self.user_id, errors=[form_message(u'Modification sauvegardées')])


    def subscribe_form(self):
        c.uid = self.user_id

        for k in ['telephoneNumber', 'cn', 'l', 'birthDate',
                  'st', 'street', 'sn',
                  'postalCode', 'mail']:
            if not getattr(self.user, k):
                c.user_id = self.user.uid
                c.need_infos = True
                return render('/subscribe_form.mako')

        c.memberships = u''.join([u"<li>%s - %i &euro;/an</li>" % (l, p) for l,p in (
                 ('Membre classique', 20),
                 (u'Tarif étudiant', 10),
                 #(ldap.CORPORATE_MEMBERSHIP, u'Tarif entreprise', 100),
                 )])

        field = lambda l, f:tag('div',
                tag('label', l)+tag('div','')+f, **{'class':'field'})

        paymentObject = (
                         (ldap.PERSONNAL_MEMBERSHIP, 'Membre classique'),
                         (ldap.STUDENT_MEMBERSHIP, u'Tarif étudiant'),
                        )
        html = field('Type', h.select('paymentObject', [ldap.PERSONNAL_MEMBERSHIP], paymentObject))
        html += field('Mode de paiement',
                h.select('paymentMode', ['cheque'],
                                (('cheque', u'Chèque'),
                                 ('paypal', 'Paypal'),
                                 ('payed', u'Pre-payé'))))
        html += field(h.literal(u'Pr&eacute;cision (si d&eacute;j&agrave; pay&eacute;)'),
                h.text('paymentComment', size='50'))
        html += h.submit('save', h.literal(u'Adh&eacute;rer'), **{'class':'context'})
        c.form = html

        # error message handling
        error = request.GET.get('error', None)
        if error == 'payed':
            errors = [u"""Vous devez pr&eacute;ciser un commentaire en cas
                      d'adh&eacute;sion pr&eacute; pay&eacute;e"""]
            c.errors = display_errors(errors)
        elif error == 'unknow':
            errors = [u"""Impossible de vous inscrire.
                      Veullez contacter l'administrateur"""]
        elif error == 'unknow':
            errors = [u"""Impossible de vous inscrire à la liste des
                      membres.  Veullez contacter l'administrateur"""]
            c.errors = display_errors(errors)
        c.user_id = self.user_id
        return render('/subscribe_form.mako')

    def subscribe(self):
        user = self.user
        paymentObject = request.POST.get('paymentObject', '')
        paymentMode = request.POST.get('paymentMode', '')
        paymentComment = request.POST.get('paymentComment', '')

        if not paymentMode:
            raise RuntimeError('No paymentMode')

        if paymentMode == 'payed' and not paymentComment.strip():
            return redirect(h.url(controller='my',
                                     action='subscribe_form',
                                     error='payed'))

        c.user = user
        c.signature = ldap.getUserByTitle('tresorier')
        c.amount = paymentObject == ldap.PERSONNAL_MEMBERSHIP and 20 or 10
        c.paymentMode = paymentMode

        paymentDate = request.POST.get('paymentDate', None)
        now = datetime.datetime.now()
        if not paymentDate:
            last_payment = [p for p in user.payments if p.paymentAmount]
            if last_payment:
                last_payment = last_payment[-1]
                d = last_payment.paymentDate
                d = h.to_python(h.to_string(d), datetime.datetime)
                if d + datetime.timedelta(365) < now:
                    paymentDate = d + datetime.timedelta(365)
            if not paymentDate:
                paymentDate = now
        paymentDate = h.to_python(h.to_string(paymentDate), datetime.date)

        if not h.DEV_MOD:
            mailman.subscribeTo('afpy-membres', user)

        payment = ldap.Payment()
        payment.paymentDate = paymentDate
        payment.paymentObject = paymentObject
        payment.paymentAmount = c.amount
        payment.invoiceReference = paymentComment
        user.append(payment)

        mail = LDAPMailTemplate(name='new_subscription',
                            subject=u"[AFPy-adhésion] Accusé de réception",
                            paymentObject=paymentObject,
                            paymentMode=paymentMode,
                            paymentComment=paymentComment,
                            )

        mail.send(user, cc='tresorerie@afpy.org')

        return render('/subscribe.mako')

    def password_form(self,errors=''):
        element = 'contents'
        errors = display_errors(errors)
        form = ''
        for name, label in (('passwd', 'Mot de passe'),
                            ('new_passwd', 'Nouveau mot de passe'),
                            ('confirm_passwd', 'Confirmation')):
            value = ''
            form += ldap_field(name, value, label=label)
        form = tag('table', form)
        form += h.submit('validate', 'Valider', class_='context')
        return tag('h1', 'Changer mon mot de passe') + \
               h.form(url=h.url.current(action='change_password'),
                       class_="remote", onsubmit="return remote_form(this);", alt=element) + \
               errors + form + h.end_form()

    def change_password(self):
        user = self.user
        passwd = request.POST.get('passwd')
        try:
            new = str(request.POST.get('new_passwd'))
            confirm = str(request.POST.get('confirm_passwd'))
        except:
            new = confirm = ''

        testing = 'paste.testing' in request.environ

        if user.check(passwd) or testing:
            if len(new) >= 6 and new == confirm:
                if not testing:
                    user.change_password(new)
                    manage_ZopeUser('edit', str(user.uid), new)

                mail = LDAPMailTemplate(name='send_password',
                                        subject='Votre password sur afpy.org',
                                        passwd=new,
                                        mfrom='www@afpy.org')
                mail.send(user.uid)
                msg = 'Mot de passe modifié. Identifiez vous'
                return redirect(
                        'http://www.afpy.org/?portal_status_message=' + msg)
            else:
                errors = [u"""Votre nouveau mot de passe doit faire au moins 6
                        caractères et être le même que la confirmation.
                        il ne doit pas contenir de caractère accentué"""]
        else:
            errors = ['Mot de passe incorect']
        return self.password_form(errors=errors)


MyController = ControllerProtector(predicates.not_anonymous())(MyController)
