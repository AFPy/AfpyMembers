# -*- coding: utf-8 -*-
<%
element = 'payments_%s' % c.user.uid
%>
<fieldset>
<legend>Paiements</legend>

%if c.message:
<div class="portalMessage">
${c.message|n}
</div>
%endif

<table width="100%" class="payments_listing listing">
${c.new.header()|n}
</table>

%for form in c.forms:
<div id="${form.model.get('paymentDate')}">
${h.form_remote_tag(url=url(controller='payments', action='edit', id=c.user.uid),
                     update=dict(success=element, failure=element))|n}
${form.render(user=c.user, h=h)|n}
${h.end_form()|n}
</div>
%endfor

${h.form_remote_tag(url=url(controller='payments', action='add', id=c.user.uid),
                     update=dict(success=element, failure=element))|n}
${c.new.render(user=c.user, h=h)|n}
${h.end_form()|n}

</fieldset>
