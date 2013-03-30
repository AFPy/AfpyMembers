# -*- coding: utf-8 -*-
<html>
  <head>
    <title>Espace membre</title>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    ${h.get_plone_skin(request, head=True)|n}
    ${h.javascript_link(request.script_name+'/javascripts/prototype.js',
			request.script_name+'/javascripts/jquery-1.3.2.min.js',
			request.script_name+'/javascripts/afpy.js')|n}
    <link rel="stylesheet" href="${request.script_name}/css/members.css" type="text/css" />
    <script type="text/javascript">
      jQuery.noConflict();
    </script>
  </head>
  <body>
    <div id="visual-portal-wrapper">
      <div>
        ${h.get_plone_skin(request)|n}
      </div>
      <div id="portal-columns" class="row">
          <div id="portal-column-content" class="cell width-3:4 position-1:4">
            <div id="letters"></div>
            <div id="contents">
                ${self.body()|n}
            </div>
          </div>
          <div id="portal-column-one">
            <div>&nbsp;</div>
            <div id="wsgi_menu"></div>
          </div>
      </div>
    </div>
    <script language="javascript">
      jQuery(document).ready(function() {
            ${h.load_html('#wsgi_menu', controller='my',action='menu',id=c.user_id)|n}
            try {loadContents();} catch (e) {};
      });
    </script>
  </body>
</html>
