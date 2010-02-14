# -*- coding: utf-8 -*-
<html>
<head>
    <title>Carte des membres</title>
    ${h.javascript_link(request.script_name+'/javascripts/jquery-1.3.2.min.js')|n}
    <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=${c.api_key|n}"
            type="text/javascript"></script>
    ${h.javascript_link(request.script_name+'/maps.js')|n}
</head>
<body onload="loadMap" onunload="GUnload()">
<h1>Cartes des membres</h1>
<p class="documentDescription">
    La carte des membres repr&eacute;sente la situation g&eacute;ographique des adh&eacute;rents de
    l'association
</p>
<div style="display:none">
    ${h.link_to('', h.url_for(action='datas'), id='data_url')|n}
    ${h.link_to('', h.url_for(action='api')+'&q=', id='geo_url')|n}
</div>
<div id="map" style="width: 100%; height: 500px"></div>
<div id="debug"></div>
</body>
</html>
