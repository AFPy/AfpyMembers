"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import cache, config, request, response
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render_mako as render
from pylons import tmpl_context as c

import members.lib.helpers as h
import members.model as model

from members.lib.afpy_helpers import *


class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        identity = environ.get('repoze.who.identity', {})
        self.user = identity.get('user')

        if self.user:
            self.user_id = c.user_id = environ['REMOTE_USER']
        else:
            self.user_id = c.user_id = None

        if self.user and 'bureau' in self.user.groups:
            self.admin = True
        else:
            self.admin = False

        c.listing_title = ''

        return WSGIController.__call__(self, environ, start_response)

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
