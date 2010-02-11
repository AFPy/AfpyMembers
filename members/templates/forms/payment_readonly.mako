<tr>
% for field in fieldset.render_fields.itervalues():
%if 'uid' not in field.name:
<td width="20%">${field.render_readonly()}</td>
%endif
% endfor
</tr>
