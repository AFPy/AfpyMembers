# -*- coding: utf-8 -*-
<div>
  <ul id="portal-personaltools">
  <%
  user = request.environ.get('afpy.user', None)
  %>
  %if user is not None:
    <li class="portalUser"><a href="http://www.afpy.org/Members/${user.uid}" id="user-name">
    ${user.uid}
    </a></li>
    <li>
    <a href="http://www.afpy.org/Members/${user.uid}/folder_contents">
    Mes documents
    </a>
    </li>
    <li>
    <a href="/membres/">
    Mes pr&eacute;f&eacute;rences
    </a>
    </li>
    <li>
    <a href="/membres/adhesion">
    Adh&eacute;sion
    </a>
    </li>
    <li>
    <a href="/membres/logout">
    Quitter
    </a>
    </li>
  %else:
    <li>
    <a href="/membres/register">
    Inscription
    </a>
    <a href="/membres/login">
    Authentification
    </a>
  </li>
  %endif
  </ul>
</div>
