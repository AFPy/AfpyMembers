# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr"
      lang="fr">
  <head>
    <title></title>

    <link rel="stylesheet" type="text/css" media="screen"
          href="http://www.afpy.org/adhesion_print.css" />
    <link rel="stylesheet" type="text/css" media="print"
          href="http://www.afpy.org/adhesion_print2.css" />
  </head>
  <body>

  <div class="bandeauPrint"><a href="javascript:window.print();"><img 
src="/afpy_print.png" style="width: 627px; height: 62px; border: none;" 
/></a></div>
  <div>
  <div class="entete_gauche">    
      ${c.u.sn}<br />
      ${c.u.street}<br />
      ${c.u.postalCode}&nbsp;${c.u.l}<br />
      ${c.u.st_label}<br />
      Tel : ${c.u.telephoneNumber}
  </div>
  <div class="entete_droit">
      ${c.u.l}, le ${c.now.strftime('%d/%m/%Y')}
  </div>
  <div class="adresse">
            ASSOCIATION FRANCOPHONE PYTHON<br />
            chez ${c.t.sn}<br />
            ${c.t.street}<br />
            ${c.t.postalCode}&nbsp;${c.t.l}<br/>
            ${c.t.st_label}
  </div>
  <div class="corps">
      <p>Adhésion à l'AFPY pour <strong>${c.now.year}</strong></p>
      <p>
      Je, soussigné <strong>${c.u.sn}</strong>, déclare avoir pris connaissance
      des statuts et du réglement intérieur de l'AFPY et en accepter tous les
      termes.
      </p>
      <p>
      Je désire être
      un membre actif de l'Association Francophone PYthon.
      </p>
      <p>
      Je joins à ce courrier un chèque de <strong>20 euros</strong> libellé à
      l'ordre de l'<strong>AFPY</strong>, ce paiement est effectué au titre
      de la cotisation <strong>2008</strong></p>
      <p class="signature">
           Date :
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
           Lu et approuvé :</p>
  </div>
  </div>
  <!-- wsgi.noskin -->
  </body>
</html>

