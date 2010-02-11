%if message:
    <div class="portalMessage">
    ${message}
    </div>
%endif
% for field in fieldset.render_fields.itervalues():
<div class="field">
  <label>${field.label_text or fieldset.prettify(field.key)}</label>
  : ${field.render_readonly()}
<div>
%endfor

