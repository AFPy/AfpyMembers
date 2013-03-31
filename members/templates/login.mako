# -*- coding: utf-8 -*-
<html>
  <head>
    <title>Login</title>
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
  <%
  user = request.environ.get('repoze.who.identity', {}).get('user', None)
  came_from = request.params.get('came_from', url(controller='utils', action='login'))
  %>
    <div id="visual-portal-wrapper">
      <div>
        ${h.get_plone_skin(request)|n}
      </div>
      <div id="portal-columns" class="row">
          <div id="portal-column-content" class="cell width-3:4 position-1:4">
            <div id="letters"></div>
            <div id="contents">
<form method="post" action="${request.script_name}/do_login">

<fieldset>

<legend>Informations sur le compte</legend>

<div class="field">
<label for="login">Nom d'utilisateur</label>
<div class="formHelp"></div>
<input type="text" id="login" value="" name="login" tabindex="1" size="15"/>
</div>

<div class="field">
<label for="password">Mot de passe</label>
<div class="formHelp"></div>
<input type="password" id="password" name="password" tabindex="2" size="15"/>
</div>

<div class="formControls">
<input type="submit" value="Connexion" name="submit" tabindex="4" class="context"/>
</div>
<input type="hidden" value="${came_from}" name="came_from" />

</fieldset>

</form>
            </div>
          </div>
          <div id="portal-column-one">
            <div>&nbsp;</div>
            <div id="wsgi_menu"></div>
          </div>
      </div>
    </div>
  </body>
</html>
