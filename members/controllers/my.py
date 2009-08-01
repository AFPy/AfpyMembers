# -*- coding: utf-8 -*-
import datetime
import logging

from repoze.what import predicates
from repoze.what.plugins.pylonshq import ActionProtector
from repoze.what.plugins.pylonshq import ControllerProtector

from members.lib.base import *
from members.forms.users import UserForm, AdminUserForm
from members.forms import ValidationError
from webhelpers.rails.tags import content_tag
from afpy.core import mailman
from afpy.mail import LDAPMailTemplate
from afpy.mail.ldap import getAddress
import string, datetime

log = logging.getLogger(__name__)

tag = content_tag

MEMBER_TYPES = (
        (u'Liste des inscrits','all'),
        (u'Liste des adhérents','subscribers'),
        (u'Liste des non adhérents','membres'),
        (u'Recherche','search'),)

def form_message(message):
    return u'%s - %s' % (message, datetime.datetime.now().strftime('%H:%M:%S'))

def get_menu(menus, tag='dl', stag='dd', element='contents', **kwargs):
    html = u'<%s>' % tag
    for label, action in menus:
        html += u' <%s>' % stag
        u = action.startswith('/') and action or url(action)
        if 'no_remote' in action:
            html += h.link_to(label, u)
        else:
            html += h.load_link('#%s' % element, text=label, url_=u)
        html += u'</%s>' % stag
    html += u'</%s>' % tag
    return html.encode('utf-8')

class MyController(BaseController):

    def index(self):
        c.user_id = self.user_id
        return render('/site.mako')

    def courrier(self):
        c.u = AdminUserForm.bind(self.user)
        u = ldap.getUser('gawel')
        c.fs = AdminUserForm.bind(u)
        c.now = datetime.datetime.now()
        request.headers['x-deliverance-no-theme'] = 'true'
        request.environ['afpy.skin.none'] = True
        return render('/courrier.mako')

    def bulletin(self):
        u = ldap.getUser('gawel')
        c.fs = AdminUserForm.bind(u)
        c.fs.readonly = True
        c.now = datetime.datetime.now()
        request.headers['x-deliverance-no-theme'] = 'true'
        request.environ['afpy.skin.none'] = True
        return render('/bulletin.mako')

    def menu(self):
        """ left menu """
        user = self.user_id
        menus = ((u'Mes informations',h.url(controller='my', action='info')),
                 ('Mes Listes', h.url(controller='my', action='listes')),
                 ('Mes paiements', h.url(controller='payments',
                                             action='index')),
                 ('Mon mot de passe', h.url(controller='my', action='password_form')))

        if self.user.expired:
            menus = ((u"<span style='color:red'>Adhérer à l'afpy</span>",
                      h.url(controller='my', action='subscribe_form',
                                no_remote='true')),) + menus
        html = get_menu(menus,
                    complete=h.update_element_function('letters',
                                                        action='empty'))
        if self.admin:
            user += ' (Admin)'
            menus = [(l, h.url_for(action='letters', id=v)) for l,v in MEMBER_TYPES]
            html += get_menu(menus, element='letters',
                        complete=h.update_element_function('contents',
                                                           action='empty'))
            menus = (
                     (u"Inscription manuelle",
                      h.url(controller='admin', action='new',
                                no_remote='true')),
                     (u"Impression bulletin",
                      h.url(controller='my', action='bulletin',
                                no_remote='true', notheme='')),
                    )
            html += get_menu(menus,
                        complete=h.update_element_function('letters',
                                                            action='empty'))

        # plone presentation...
        html = html.replace('dl>','div>')
        html = html.replace('<dd>','<div class="nav1">')
        html = html.replace('</dd>','</div>')
        return """
        <div class="portlet">
            <h5>Espace de %s</h5>
            <div class="portletBody">
            %s
            </div>
        </div><div>&nbsp;</div>
        """ % (user, html)

    @ActionProtector(predicates.in_group('bureau'))
    def letters(self, id='all'):
        """ letters menu """
        stype = id
        for label,v in MEMBER_TYPES:
            if stype == v:
                break
        if v == 'search':
            form = h.form_remote_tag(
                   url=h.url(controller='my', action='subscribers',
                                 stype='search', letter='all'),
                   update=dict(success='contents', failure='contents'))
            contents = form + h.text_field('letter') + \
                       h.submit('Rechercher') + h.end_form()
        else:
            menus = [(l.upper(), h.url(controller='my', action='subscribers',
                                       stype=stype,letter=l)) \
                    for l in string.ascii_lowercase]
            contents = get_menu(menus, tag='div', stag='span')
        return tag('h1', label) + tag('fieldset',
                                      tag('legend', 'Navigation') + \
                   contents)

    def info(self, id='', message=None):
        """ user form """
        user = id and ldap.getUser(id) or self.user
        admin = self.admin

        html = title = ''
        if user != self.user and not admin:
            raise NotAuthorizedError()

        if admin:
            fs = AdminUserForm.bind(user)
        else:
            fs = UserForm.bind(user)
        if message:
            e = ValidationError(message)
            fs._errors = [e]
        html += fs.render()

        if admin and self.user != user:
            element = 'infos_%s' % user.uid
            hidden = h.hidden_field('uid',user.uid)
        else:
            element = 'contents'
            hidden = ''
        form = h.form_remote_tag(url=h.url_for(action='save_info',id=None),
                                 update=dict(success=element, failure=element))

        html = title + tag('fieldset', tag('legend', u'Mes informations') + \
                form + hidden + tag('table', html) + \
                h.submit("Sauver", name='save',
                         **{'class':'context'}) + '</form>')
        return html

    def save_info(self):
        """ save user form """
        admin = self.admin
        uid = request.POST.get('uid')
        if admin and uid:
            user = ldap.getUser(uid)
        else:
            user = self.user
        fs = admin and AdminUserForm or UserForm
        fs = fs.bind(user, data=request.POST)
        if fs.validate():
            fs.sync()
            user.save()
            message = form_message(u'Modifie').encode('utf-8')
        else:
            message = None
        return self.info(id=user.uid, message=message)

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
        html += content_tag('legend', 'Listes de diffusion')
        html += display_errors(errors)
        html += h.form_remote_tag(url=h.url_for(action='save_listes',id=None),
                                 update=dict(success=element, failure=element))
        html += hidden

        email = user.email
        selected = mailman.lists.getListsFor(email)
        for ml in mailman.lists.values():
            # hide private list if not subbcribed
            if not admin and not ml.public and ml.name not in selected:
                continue
            html += '<div>'
            html += h.check_box('selected',
                                id=ml.name,
                                checked=ml.name in selected,
                                value=ml.name)
            html += ' '
            html += content_tag('label', ml.title, **{'for':ml.name})
            html += ' ('
            html += h.link_to('infos',
                         'http://lists.afpy.org/mailman/listinfo/%s' % ml.name)
            html += ')'
            html += '</div>'

        html += content_tag('div', '&nbsp;')
        html += h.submit('Sauver', **{'class':'context'})
        html += h.end_form()

        return content_tag('fieldset', html)

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

    @ActionProtector(predicates.in_group('bureau'))
    def subscribers(self, stype='', letter=''):
        """ get subscribers listing """
        if stype == 'members':
            f = '(&(!(membershipExpirationDate=*))(uid=%s*))' % letter
        elif stype == 'subscribers':
            f = '(&(membershipExpirationDate=*)(uid=%s*))' % letter
        elif stype == 'search':
            letter = request.POST['letter']
            f = '(&(objectClass=person)(sn=*%s*))' % letter
        else:
            f = '(&(objectClass=person)(uid=%s*))' % letter
        conn = ldap.get_conn()
        res = conn.search_nodes(filter=f, attrs=['uid'])
        members = [m.uid for m in res]
        members.sort()
        c.members = members
        return render('/listing.mako')

    def subscribe_form(self):
        c.uid = self.user_id

        for k in ['telephoneNumber', 'cn', 'l', 'birthDate',
                  'st', 'street', 'sn',
                  'postalCode', 'mail']:
            if not getattr(user, k):
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

        paymentObject = h.options_for_select((
                         ('Membre classique', ldap.PERSONNAL_MEMBERSHIP),
                         (u'Tarif étudiant', ldap.STUDENT_MEMBERSHIP),
                            ))
        html = field('Type', h.select('paymentObject', paymentObject))
        html += field('Mode de paiement',
                h.select('paymentMode',
                    h.options_for_select(
                                ((u'Chèque','cheque'),
                                 ('Paypal', 'paypal'),
                                 (u'Pre-payé', 'payed')), 'cheque')))
        html += field(u'Pr&eacute;cision (si d&eacute;j&agrave; pay&eacute;)',
                h.text_field('paymentComment', size='50'))
        html += h.submit(u'Adh&eacute;rer', **{'class':'context'})
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
        paymentObject = request.POST.get('paymentObject')
        paymentMode = request.POST.get('paymentMode')
        paymentComment = request.POST.get('paymentComment')

        if not paymentMode:
            raise RuntimeError('No paymentMode')

        if paymentMode == 'payed' and not paymentComment.strip():
            return redirect_to('http://www.afpy.org'+ \
                    h.url_for(controller='my',
                              action='subscribe_form',
                              error='payed'))

        member=user.getMemberData()
        address=getAddress('tresorier')

        c.user = user
        c.address = address.replace('\n', '<br />')
        c.amount = paymentObject == ldap.PERSONNAL_MEMBERSHIP and 20 or 10
        c.paymentMode = paymentMode

        paymentDate = None
        now = datetime.datetime.now()
        last_payment = user.lastRealPayment()
        if last_payment:
            d = last_payment.get('paymentDate')
            if d + datetime.timedelta(365) < now - datetime.timedelta(90):
                paymentDate = d + datetime.timedelta(365)
        if not paymentDate:
            paymentDate = now

        if mailman.subscribeTo('afpy-membres', user) > 0:
            return redirect_to('http://www.afpy.org'+ \
                    h.url_for(controller='my',
                              action='subscribe_form',
                              error='mailman'))

        user.addPayment(paymentDate=paymentDate,
                        paymentAmount=0,
                        paymentObject=paymentObject,
                        invoiceReference='awaiting')

        mail = LDAPMailTemplate(name='new_subscription',
                            subject=u"[AFPy-adhésion] Accusé de réception",
                            signature='tresorier',
                            member=member,
                            address=address,
                            paymentObject=paymentObject,
                            paymentMode=paymentMode,
                            paymentComment=paymentComment,
                            )

        if '/test_' in request.environ['SCRIPT_NAME']:
            mail.send(user, cc='www@afpy.org')
        else:
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
        form += h.submit('Valider', name='validate', **{'class':'context'})
        return tag('h1', 'Changer mon mot de passe') + \
               h.form_remote_tag(url=h.url_for(action='change_password'),
                   update=dict(success=element, failure=element)) + \
               errors + form + h.end_form()

    def change_password(self):
        user = self.user
        passwd = request.POST.get('passwd')
        try:
            new = str(request.POST.get('new_passwd'))
            confirm = str(request.POST.get('confirm_passwd'))
        except:
            new = confirm = ''

        try:
            user.check(passwd)
        except:
            errors = ['Mot de passe incorect']
        else:
            if len(new) >= 6 and new == confirm:
                ldap.changePassword(user.uid, new)
                manage_ZopeUser('edit', str(user.uid), new)

                mail = LDAPMailTemplate(name='send_password',
                                        subject='Votre password sur afpy.org',
                                        passwd=new,
                                        mfrom='www@afpy.org')
                mail.send(user.uid)
                msg = 'Mot de passe modifié. Identifiez vous'
                return redirect_to(
                        'http://www.afpy.org/?portal_status_message=' + msg)
            else:
                errors = [u"""Votre nouveau mot de passe doit faire au moins 6
                        caractères et être le même que la confirmation.
                        il ne doit pas contenir de caractère accentué"""]
        return self.password_form(errors=errors)


MyController = ControllerProtector(predicates.not_anonymous())(MyController)
