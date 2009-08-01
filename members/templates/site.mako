# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<script language="javascript">
var loadContents = function() {
    var url = "${h.url_for(controller='my',action=None)|n}";
    url = url.split('/my')[0];
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
    new Ajax.Updater('contents', 
                     url+'/'+controller+'/'+action+'/'+user, 
                     {asynchronous:true, evalScripts:true});
}
</script>
