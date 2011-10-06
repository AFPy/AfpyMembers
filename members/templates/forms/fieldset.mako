<%
_ = F_
_focus_rendered = False
%>\

% for error in fieldset.errors.get(None, []):
<div class="portalMessage">
  ${_(str(error))}
</div>
% endfor

% for field in fieldset.render_fields.itervalues():
  % if field.requires_label:
<div class="field">
  <label for="${field.renderer.name}">${field.label_text or fieldset.prettify(field.key)}</label>
  %if field.is_required():
      <span class="field_req">*</span>
  %endif
  <div></div>
  ${field.render()|n}
  <div class="formHelp">
  % for error in field.errors:
  <span class="field_error">${_(str(error))}</span>
  % endfor
  </div>
</div>
  % else:
${field.render()|n}
  % endif
% endfor

