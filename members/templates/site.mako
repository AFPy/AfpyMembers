# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<script language="javascript">
var loadContents = function() {
    var root = "${request.script_name}";
    var user = "${c.user_id}";
    var parts = window.location.href.split('#');
    var controller = 'my';
    var action = 'info';
    if (parts.length > 1)
        action = parts[1];
    switch (action) {
        case "listes":
            break;
        case "payments":
            controller="payments";
            action="index"
            break;
        case "password":
            action = 'password_form';
            break;
        default:
            action = 'info';
            break;
    }
    jQuery('#contents').load(root+'/'+controller+'/'+action); 
}
</script>
