<table width="100%" class="payments_listing listing">
<tr>
% for field in fieldset.render_fields.itervalues():
<td ${'paymentAmount' not in field.name and 'width="150"' or ''}
    align="center">
    %if field.is_readonly():
        ${field.render_readonly()|n}
        <div style="display:none">
        ${field.render()|n}
        </div>
    %else:
        ${field.render()|n}
    %endif
</td>
% endfor
<td>
%if fieldset.model._pk:
<div>
<input type="hidden" name="dn" value="${fieldset.model._dn}" />
<a href="${h.url('edit_payment', id=user.uid, paymentDate=fieldset.model._pk)}" alt="payments_${user.uid}">Sauver</a>
</div>
<div>
<a href="${h.url('delete_payment', id=user.uid, paymentDate=fieldset.model._pk)}" alt="payments_${user.uid}">Supprimer</a>
</div>
%else:
<input type="submit" class="context" value="Ajouter" />
%endif
</td>
</tr>
</table>

