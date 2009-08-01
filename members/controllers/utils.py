import logging

from members.lib.base import *

log = logging.getLogger(__name__)

class UtilsController(BaseController):

    def personnal_bar(self):
        return render('/personnal_bar.mako')

    def login(self):
        return render('/login.mako')

    def error(self):
        raise RuntimeError('test error is raised and sent by email')
