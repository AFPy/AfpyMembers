import re
import urllib
import logging
from datetime import datetime
from cPickle import load
from members.lib.base import *
from afpy.core import config
from afpy.core.countries import COUNTRIES

log = logging.getLogger(__name__)

filename = '/tmp/google.maps.coords.dump'
api_key = config.get('api_keys', 'maps.google.com')


class MapsController(BaseController):

    def index(self):
        c.api_key = api_key
        return render('/maps.mako')

    @jsonify
    def datas(self):
        conn = ldap.get_conn()
        users = conn.search_nodes(filter='(&(postalCode=*)(street=*))',
                    attrs=['uid', 'street', 'postalCode', 'l', 'st'])
        datas = {}
        if os.path.isfile(filename):
            coords = load(open(filename))
        else:
            coords = {}
        for user in users:
            try:
                short_address = u'%s, %s' % (
                        user.postalCode.strip(),
                        user.st.strip())
            except UnicodeDecodeError, e:
                log.error('%r %s - %s', e, e, user)
                coord = None
            else:
                coord = coords.get(short_address)
            if coord:
                datas[short_address] = datas.get(short_address, []) + [user['uid']]
        return {'result':[dict(point=[coords[k].get('lng'), coords[k].get('lat')], address=k,
                     users=''.join(['<div>%s</div>' % u for u in v])
                     ) for k, v in datas.items()]}

