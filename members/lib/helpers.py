"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
# Import helpers as desired, or define your own, ie:
# from webhelpers.html.tags import checkbox, password
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

def load_link(element, text='+', url_=None, **kwargs):
    return '<a href="javascript:void(0)" onclick="jQuery(%r).load(%r);">%s</a>' % (element, url_ or url(**kwargs), text)

def close_link(element):
    return '<a href="javascript:void(0);" onclick="jQuery(%r).empty();">-</a>' % element

