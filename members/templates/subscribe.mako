# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<h1>
Confirmation d'inscription
</h1>

<p>
Un courriel vous a été envoyé récapitulant les informations que vous venez de
saisir.
</p>

% if c.paymentMode != 'payed':
<p>
Vous y retrouverez aussi les informations ci-dessous nécessaires à la validation
 de votre adhésion
</p>

<h1>Et maintenant ?</h1>

%if c.paymentMode == 'paypal':
<p>Vous avez choisis de régler via Paypal.</p>
<p>Pour confirmer votre adhésion, vous devez maintenant vous rendre sur le site
 Paypal en cliquant sur le bouton ci-dessous</p>
<form name="_xclick" action="https://www.paypal.com/fr/cgi-bin/webscr" method="post">
    <input type="hidden" name="cmd" value="_xclick">
    <input type="hidden" name="business" value="tresorier@afpy.org">
    <input type="hidden" name="currency_code" value="EUR">
    <input type="hidden" name="item_name" value="Adhesion ${c.user.sn} (${c.user.uid} / ${c.user.mail})">
    <input type="hidden" name="amount" value="${c.amount}">
    <input type="image"
           src="http://www.paypal.com/fr_FR/i/btn/x-click-but01.gif" border="0"
           name="submit"
           alt="Effectuez vos paiements via PayPal : une solution rapide, gratuite et sécurisée">
</form>
% endif

% if c.paymentMode == 'cheque':
<p>Pour confirmer votre adhésion, vous devez maintenant nous faire parvenir
 votre réglement</p>
<p>Vous avez choisis de régler par chèque. Veuillez nous faire parvenir votre
 chèque à:
</p>
<pre>
Association Francophone Python
A l'attention de ${c.signature.sn}, ${c.signature.title.title()} de l'association
${c.signature.street}
${c.signature.postalCode} ${c.signature.l}, France
</pre>
% endif

% endif
