var remote_form = function(form) {
    var form = jQuery(form);
    var url = form.attr('action');
    var element = jQuery('#'+form.attr('alt'));
    jQuery.post(url, form.serialize(), function(data) { element.html(data); });
    return false;
}

jQuery(document).ready(function() {
    jQuery('form.remote').submit(function () {return remote_form(this)});
});
