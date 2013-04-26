import os
import logging
from cPickle import load
from members.lib.base import *  # NOQA
from afpy.core import config
from pylons.decorators.cache import beaker_cache

log = logging.getLogger(__name__)

filename = '/tmp/google.maps.coords.dump'
api_key = config.get('api_keys', 'maps.google.com')


class MapsController(BaseController):

    def index(self):
        c.api_key = api_key
        return render('/maps.mako')

    @beaker_cache()
    @jsonify
    def datas(self):
        conn = ldap.get_conn()
        users = []
        for i in range(1, 10):
            users.extend(conn.search_nodes(
                filter='(&(postalCode=%s*)(street=*))' % i,
                attrs=['uid', 'street', 'postalCode', 'l', 'st']))
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
                datas[short_address] = datas.get(short_address, []) + \
                    [user.uid]
        return {'result': [dict(point=[coords[k].get('lng'),
                                coords[k].get('lat')], address=k,
                                users=''.join(['<div>%s</div>' % u for u in v])
                                ) for k, v in datas.items()]}
