# -*- coding: utf-8 -*-
<html>
  <head>
    ${h.javascript_include_tag(builtins=True)|n}
  </head>
  <body onload="
                ">
    <h1>Formulaire d'inscription</h1>
    <p class="documentDescription">&nbsp;</p>
    <div id="register_form"></id>
    <script language="javascript">
    ${h.remote_function(update='register_form',
                        url=h.url(controller='register',action='register'))|n}
    </script>
  </body>
</html>

