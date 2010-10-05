import logging
from pylons import request
from webob import exc

from members.lib.base import *

log = logging.getLogger(__name__)

class UtilsController(BaseController):

    def personnal_bar(self):
        return render('/personnal_bar.mako')

    def login(self):
        came_from = request.params.get('came_from')
        if self.user and came_from and 'members' not in came_from:
            return exc.HTTPFound(location=came_from)(request.environ, self.start_response)
        return render('/login.mako')

    def error(self):
        raise RuntimeError('test error is raised and sent by email')
