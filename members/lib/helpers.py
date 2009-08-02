# -*- coding: utf-8 -*-
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
# Import helpers as desired, or define your own, ie:
# from webhelpers.html.tags import checkbox, password
import os
from webhelpers import *
from webhelpers.rails import *
from webhelpers.rails.tags import *
from webhelpers.rails.urls import *
from webhelpers.rails.form_tag import *
from webhelpers.rails.asset_tag import *
from webhelpers.rails.prototype import *
from routes import url_for
from pylons import url
from afpy.ldap import custom as ldap
from afpy.ldap.utils import to_string, to_python

def load_html(element, **kwargs):
    return 'jQuery(%r).load(%r);' % (element, url(**kwargs))

def load_link(element, text='+', url_=None, empty=None, **kwargs):
    if empty:
        return '''<a href="javascript:void(0)" onclick="jQuery(%r).empty();jQuery(%r).load(%r);">
                  %s</a>''' % (empty, element, url_ or url(**kwargs), text)
    else:
        return '<a href="javascript:void(0)" onclick="jQuery(%r).load(%r);">%s</a>' % (element, url_ or url(**kwargs), text)

def close_link(element):
    return '<a href="javascript:void(0);" onclick="jQuery(%r).empty();">-</a>' % element

DEV_MOD = not os.path.isdir('/home/afpy')

MEMBER_TYPES = (
        (u'Liste des inscrits','all'),
        (u'Liste des adhérents','subscribers'),
        (u'Liste des non adhérents','membres'),
        (u'Recherche','search'),)


def get_menu(menus, tag='dl', stag='dd', element='contents', empty=None, **kwargs):
    html = u'<%s>' % tag
    for label, action in menus:
        html += u' <%s>' % stag
        u = action.startswith('/') and action or url(action)
        if 'no_remote' in action:
            html += link_to(label, u)
        else:
            if empty and not empty.startswith('#'):
                empty = '#%s' % empty
            if element and not element.startswith('#'):
                element = '#%s' % element
            html += load_link(element, text=label, url_=u, empty=empty)
        html += u'</%s>' % stag
    html += u'</%s>' % tag
    return html.encode('utf-8')
