<%def name="line(uid)">
<fieldset>
<div id="${uid}">
    <b style="font-size:120%">${uid}</b>
    (infos
    ${h.link_to_remote('+', dict(update='infos_%s' % uid,
                       url=h.url_for(action='info', id=uid)))|n}
    /
    ${h.link_to_function('-', h.update_element_function(
                                'infos_%s' % uid, action='empty'))|n}
    )

    (listes
    ${h.link_to_remote('+', dict(update='listes_%s' % uid,
                        url=h.url_for(action='listes', id=uid)))|n}
    /
    ${h.link_to_function('-',
        h.update_element_function('listes_%s' % uid, action='empty'))|n}
    )

    (paiements
    ${h.link_to_remote('+', dict(update='payments_%s' % uid,
                         url=h.url_for(controller='payments',
                         action='edit', id=uid)))|n}
    /
    ${h.link_to_function('-',
       h.update_element_function('payments_%s' % uid, action='empty'))|n}

    )
</div>
<div id="infos_${uid}"></div>
<div id="listes_${uid}"></div>
<div id="payments_${uid}"></div>
</fieldset>
</%def>

%if not c.members:
<div>Aucuns resultats</div>
%endif
%for uid in c.members:
${line(uid)|n}
%endfor

