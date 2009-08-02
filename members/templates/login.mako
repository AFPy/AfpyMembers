# -*- coding: utf-8 -*-
<html>
  <head>
  </head>
  <body>
  <%
  user = request.environ.get('repoze.who.identity', {}).get('user', None)
  came_from = request.params.get('came_from', url(controller='utils', action='login'))
  %>
%if user is not None:
    <h1>Bienvenu ${user.cn}. Vous êtes maintenant identifié</h1>
%else:
    <h1>Authentification</h1>
    <p class="documentDescription">&nbsp;</p>
  
<form method="post" action="${request.environ.get('SCRIPT_NAME', '')}/do_login">

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
%endif
  </body>
</html>


