# -*- coding: utf-8 -*-
<html>
  <head>
    <title>Espace membre</title>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    ${h.javascript_include_tag('/javascripts/prototype.js')|n}
    ${h.javascript_include_tag('/javascripts/jquery-1.3.2.min.js')|n}
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
  <body>
    %if request.GET.get('wsgi_menu'):
    <div id="wsgi_menu"></div>
    %endif
    <div id="content">
    <div id="letters"></div>
    <div id="contents">
        ${self.body()|n}
    </div>
    <script language="javascript">
    ${h.load_html('#wsgi_menu', controller='my',action='menu',id=c.user_id)}
    try {loadContents();} catch (e) {};
    </script>
    </div>
  </body>
</html>
