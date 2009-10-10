# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<h1>Formulaire d'adhésion</h1>

${c.errors|n}

<p>
 Je désire <b>contribuer au développement</b> de Python et <b>participer à la
 vie associative</b> de l'afpy et donc, (re)devenir membre actif de
 l'association.
</p>

%if c.need_infos:
    <p>
    Avant d'adhérer, je remplis mes
    ${h.link_to('informations', h.url_for(action="index", id=c.user))|n}
    </p>
%else:

    <p>
     J'enverrai mon paiement par chèque ou via le formulaire
     Paypal (Visa/Mastercard/Compte Paypal) prévu à cet effet
    </p>
    <p>
    Je choisis l'une des deux options:
        <ul>
        ${c.memberships|n}
        </ul>
    </p>
    <p>Je prends bien note que mon adhésion ne prendra effet qu'a 
     réception du paiement. Ainsi que du 
     ${h.link_to('courier de confirmation',
                 h.url_for(action='courrier', notheme='true'))|n}
     si c'est ma première adhésion.</p>

    ${h.form(h.url_for(controller='my', action='subscribe', id=None))|n}
    <fieldset>
    <legend>Adhésion</legend>

    ${c.form|n}

    </fieldset>
    ${h.end_form()|n}

%endif
