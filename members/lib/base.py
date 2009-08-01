"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render_mako as render

import members.lib.helpers as h
import members.model as model

from members.lib.afpy_helpers import *
from members.lib.permissions import *


class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        self.user = environ.get('afpy.user', None)

        if self.user:
            self.user_id = environ['REMOTE_USER']

        if self.user and self.user.uid.lower() in AdminUser.users:
            self.admin = True
        else:
            self.admin = False

        return WSGIController.__call__(self, environ, start_response)

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
