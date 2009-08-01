# -*- coding: utf-8 -*-
<html>
<head>
    ${h.javascript_include_tag('/jquery.js')|n}
    <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=${c.api_key|n}"
            type="text/javascript"></script>
    ${h.javascript_include_tag('/maps.js')|n}
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
