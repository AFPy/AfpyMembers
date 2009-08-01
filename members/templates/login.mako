# -*- coding: utf-8 -*-
<html>
  <head>
  </head>
  <body>
  <%
  user = request.environ.get('afpy.user', None)
  %>
%if user is not None:
    <h1>Bienvenu ${user.cn}. Vous êtes maintenant identifié</h1>
%else:
    <h1>Authentification</h1>
    <p class="documentDescription">&nbsp;</p>
  
<form method="post" action="/do_login?came_from=/">

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
<input type="hidden" value="/membres/login" name="came_from" />

</fieldset>

</form>
%endif
  </body>
</html>


