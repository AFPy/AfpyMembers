# -*- coding: utf-8 -*-
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
# Import helpers as desired, or define your own, ie:
# from webhelpers.html.tags import checkbox, password
import os
from webhelpers import *  # noqa
from webhelpers.html.tags import *  # noqa
from webhelpers.html import *  # noqa
from webhelpers.html import literal
from pylons import url
from BeautifulSoup import BeautifulSoup
from pyquery import PyQuery
from afpy.ldap import custom as ldap  # noqa
from afpy.ldap.utils import to_string, to_python  # noqa


def load_html(element, **kwargs):
    return 'jQuery(%r).load(%r);' % (element, url(**kwargs))


def load_link(element, text='+', url_=None, empty=None, **kwargs):
    if empty:
        return literal('''
            <a href="javascript:void(0)"
            onclick="jQuery(%r).empty();jQuery(%r).load(%r);">
            %s</a>''' % (empty, element, url_ or url(**kwargs), text))
    else:
        return literal('''<a href="javascript:void(0)"
            onclick="jQuery(%r).load(%r);">%s</a>
            ''' % (element, url_ or url(**kwargs), text))


def close_link(element):
    return literal('''<a href="javascript:void(0);"
                            onclick="jQuery(%r).empty();">-</a>''' % element)

DEV_MOD = not os.path.isdir('/home/afpy')

MEMBER_TYPES = (
    (u'Liste des inscrits', 'all'),
    (u'Liste des adhérents', 'subscribers'),
    (u'Liste des non adhérents', 'membres'),
    (u'Recherche', 'search'),)


def get_menu(menus, tag='dl', stag='dd', element='contents',
             empty=None, **kwargs):
    html = literal('')
    for label, action in menus:
        html += literal(' <%s class="portletItem">' % stag)
        u = action.startswith('/') and action or url(action)
        if 'no_remote' in action:
            html += link_to(label, u)
        else:
            if empty and not empty.startswith('#'):
                empty = '#%s' % empty
            if element and not element.startswith('#'):
                element = '#%s' % element
            html += load_link(element, text=label, url_=u, empty=empty)
        html += literal('</%s>' % stag)
    return html


def get_plone_skin(request, head=False):
    key = 'plone.data'
    if key not in request.environ:
        url = 'http://dev.afpy.org'
        doc = PyQuery(url=url)
        doc('#portal-searchbox, #portal-personaltools-wrapper').remove()
        data = {}
        nodes = doc('style, link')
        value = '\n'.join([str(n) for n in nodes.items()])
        data['head'] = value
        value = str(doc('#portal-top'))
        data['header'] = value
        request.environ[key] = data
    if head:
        return request.environ[key]['head']
    else:
        return request.environ[key]['header']
