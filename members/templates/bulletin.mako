# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr"
      lang="fr">
  <head>
    <title></title>
    <link rel="stylesheet" type="text/css" media="screen"
          href="${request.script_name}/css/adhesion_print.css" />
    <link rel="stylesheet" type="text/css" media="print"
          href="${request.script_name}/css/adhesion_print2.css" />
  </head>
  <body onload="javascript:window.print();"
  <div class="entete_gauche">
      Login afpy.org :<br />
      Courriel :<br />
      Nom :<br />
      Prénom :<br />
      Date de naissance :<br />
      Adresse :<br />
      Code postal :<br />
      Ville :<br />
      Pays :<br />
      Tél. :
  </div>
  <div class="entete_droit">
      ........., le ${c.now.strftime('%d/%m/%Y')}
  </div>
  <div class="adresse">
            ASSOCIATION FRANCOPHONE PYTHON<br />
            chez ${c.fs.sn.render_readonly()}<br />
            ${c.fs.street.render_readonly()}<br />
            ${c.fs.postalCode.render_readonly()}&nbsp;${c.fs.l.render_readonly()}<br/>
            ${c.fs.st.render_readonly()}
  </div>
  <div class="corps">
      <p>Adhésion à l'AFPY pour <strong>${c.now.year}</strong></p>
      <p>
      Je, soussigné <strong>____________________</strong>,
      déclare avoir pris connaissance
      des statuts et du réglement intérieur de l'afpy et en accepter tous les
      termes.
      </p>
      <p>
      Je désire être
      un membre actif de l'Association Francophone PYthon.
      </p>
      <p>
      Je joins à ce courrier un chèque de <strong>20 euros</strong> libellé à
      l'ordre de l'<strong>AFPY</strong>, ce paiement est effectué au titre
      de la cotisation <strong>${c.now.strftime('%Y')}</strong></p>
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

