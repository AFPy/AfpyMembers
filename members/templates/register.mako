# -*- coding: utf-8 -*-
<html>
  <head>
    <title>Formulaire d'inscription</title>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    ${h.javascript_link(request.script_name+'/javascripts/prototype.js',
			request.script_name+'/javascripts/jquery-1.3.2.min.js',
			request.script_name+'/javascripts/afpy.js')|n}
    <script type="text/javascript">
      jQuery.noConflict();
    </script>
    <style type="text/css">
    td#portal-column-two { display:none; }
    div#menu dl,
    div#menu dd,
    div#menu_admin dl,
    div#menu_admin dd
    {
        margin:0;
        padding:0;
    }
    div#menu_admin dl{
        margin-top:1em;
    }
    .field_req {
        color:red;
    }
    .payments_listing {
        margin:0 !important;
    }
    </style>
  </head>
  <body onload="
                ">
    <h1>Formulaire d'inscription</h1>
    <p class="documentDescription">&nbsp;</p>
    <div id="register_form"></id>
    <script language="javascript">
    jQuery('#register_form').load("${h.url(controller='register',action='register')}");
    </script>
  </body>
</html>

