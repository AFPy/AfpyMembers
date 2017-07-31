<%def name="line(uid)">
<fieldset>
<div id="${uid}">
    <b style="font-size:120%">${uid}</b>
    (infos
    ${h.load_link('#infos_%s' % uid, controller='my', action='info', id=uid)|n}
    /
    ${h.close_link('#infos_%s' % uid)|n}
    )

    <!-- wait for 2021
    (listes
    ${h.load_link('#listes_%s' % uid, controller='my', action='listes', id=uid)|n}
    /
    ${h.close_link('#listes_%s' % uid)|n}
    )
    -->

    (paiements
    ${h.load_link('#payments_%s' % uid, controller='payments', action='edit', id=uid)|n}
    /
    ${h.close_link('#payments_%s' % uid)|n}

    )
</div>
<div id="infos_${uid}"></div>
<div id="listes_${uid}"></div>
<div id="payments_${uid}"></div>
</fieldset>
</%def>
%if c.listing_title:
<h1>${c.listing_title}</h1>
%endif
%if not c.members:
<div>Aucuns resultats</div>
%endif
%for uid in c.members:
${line(uid)|n}
%endfor

