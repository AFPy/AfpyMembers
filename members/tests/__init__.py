"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest import TestCase

from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import config, url
from routes.util import URLGenerator
from webtest import TestApp
from afpy.ldap import custom as ldap
from iw.email.testing import EmailTestCase

import pylons.test

__all__ = ['environ', 'url', 'TestController', 'admin_environ']

# Invoke websetup with the current config file
SetupCommand('setup-app').run([config['__file__']])

environ = {}
admin_environ = {'REMOTE_USER':'gawel',
                 'repoze.who.identity': dict(
                     user=ldap.getUser('gawel'),
                     userid='gawel'),
                'repoze.what.credentials': dict(
                    groups=("bureau",),
                    permissions=[],
                    ),
                }

class TestController(EmailTestCase):

    def __init__(self, *args, **kwargs):
        if pylons.test.pylonsapp:
            wsgiapp = pylons.test.pylonsapp
        else:
            wsgiapp = loadapp('config:%s' % config['__file__'])
        self.app = TestApp(wsgiapp)
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)

