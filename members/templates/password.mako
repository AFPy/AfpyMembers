# -*- coding: utf-8 -*-
<html>
  <head>
    ${h.javascript_include_tag(builtins=True)|n}
  </head>
  <body onload="
                ">
    <h1>Perte de mot de passe</h1>
    <div id="password_form"></id>
    <script language="javascript">
    ${h.remote_function(update='password_form',
                       url=h.url(controller='password',action='password_form'))|n}
    </script>
  </body>
</html>

