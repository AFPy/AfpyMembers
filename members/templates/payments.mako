# -*- coding: utf-8 -*-
<fieldset>
<legend>Mes paiements</legend>
%if c.user.membershipExpirationDate:
<p class="documentDescription">Votre cotisation expire le
${c.user.membershipExpirationDate.strftime('%d/%m/%Y')}
</p>
%endif
<table class="listing">
${c.forms[0].header()|n} 
%for form in c.forms:
${form.render()|n} 
%endfor
</table>
</fieldset>
