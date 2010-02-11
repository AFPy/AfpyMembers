# -*- coding: utf-8 -*-
import os, sys, logging, xmlrpclib
from members.lib.base import h
from webhelpers.html.tags import *
from pylons import request
from afpy.ldap import custom as ldap
from afpy.core import config
from afpy.core.countries import COUNTRIES
from base64 import encodestring, decodestring
from urllib import quote, unquote
import socket

COUNTRIES_OPTIONS = [(v.decode('utf-8'),k) for k,v in COUNTRIES.items()]

def tag(name, *args, **kwargs):
    return h.HTML.tag(name, *args, **kwargs)

def manage_ZopeUser(action, name, passwd='', manager=0):
    """ @action: add | edit | delete
    """
    try:
        request.path_info
    except TypeError:
        pass
    else:
        if 'paste.testing' in request.environ:
            return True

    user = ldap.getUser(name)
    groups = user.groups
    if 'cd' in groups or 'bureau' in groups:
        manager = 1
    try:
        server = xmlrpclib.Server('%s/ldap/' % config.zope_admin_url())
        return server.manage_User(action, user.cn or user.uid, passwd, manager)
    except xmlrpclib.Fault, e:
        pass
    except socket.error:
        pass

def ldap_field(name, value, allowed=True, label=None):
    if label is None:
        if label == 'passwd':
            label = 'Mot de passe'
    if 'date' in name.lower():
        if value:
            value = value.strftime('%d/%m/%Y')
    field = tag('td', tag('label',label, **{'for':name}))
    if allowed == True:
        if 'passwd' in name:
            field += tag('td', h.password(name, value=value))
        elif name == 'st':
            field += tag('td', h.select(name, [value], COUNTRIES_OPTIONS))
        else:
            field += tag('td', h.text(name, value=value))
    else:
        field += tag('td', value)
    return tag('tr',field)



def display_errors(errors):
    html = h.literal('')
    if errors:
        for error in errors:
            html += tag('div', error)
    if not html:
        return ''
    return h.literal('<div class="portalMessage">%s</div><div>&nbsp;</div>') % html

