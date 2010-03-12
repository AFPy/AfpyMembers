# -*- coding: utf-8 -*-
from IPython.Shell import IPShellEmbed
import afpy.ldap.custom as ldap
from optparse import OptionParser
import sys

class Users(dict):
    def update(self, users):
        for u in users:
            self[u.uid] = u
            self.__dict__[u.uid] = u
    def __getattr__(self, attr):
        return self.get(attr)
    def __repr__(self):
        return repr(sorted(self.keys()))

class User(ldap.User):

    def __str__(self):
        out = []
        def g(name):
            return getattr(self, name, None)
        title = '%s (%s)' % (self.sn, self.uid)
        out.append(title)
        out.append("-"*len(title))
        for name in ('uid', 'mobile', 'mail', 'membershipExpirationDate'):
            v = g(name)
            if v:
                if isinstance(v, basestring):
                    v = v.replace('$', '\n         ')
                title = ldap.User.__dict__[name].title
                out.append('%-7.7s: %s' % (title, v))
        return '\n'.join([o.encode('utf-8') for o in out if o])

def search(name):
    conn = ldap.get_conn()
    if name:
        filter = '(|(uid=*%(name)s*)(cn=*%(name)s*))' % dict(name=name)
    else:
        filter = 'uid=*'
    return conn.search_nodes(node_class=User, filter=filter)


def main():
    parser = OptionParser()
    parser.add_option("-g", "--grep", dest="grep",
                      default=None, metavar='NAME',
                      help="search for NAME")
    parser.add_option("-i", "--interactive", dest="interactive",
                      action="count", default=0,
                      help='Start an ipython session')
    parser.add_option("-v", "--verbose", dest="verbose",
                      action="count", default=0)
    options, args = parser.parse_args()

    u = None
    users = Users()

    if not options.grep and not options.interactive:
        parser.parse_args(['-h'])

    if options.grep:
        results = search(options.grep != '*' and options.grep or '')
        results.sort(cmp=lambda a, b: cmp(a.cn, b.cn))
        users.update(results)
        for u in results:
            if u:
                print u
                print ''
        if results:
            u = results[0]

    if options.interactive:
        sys.argv = sys.argv[0:1]
        ipshell = IPShellEmbed()
        __IPYTHON__.api.to_user_ns('ldap')
        __IPYTHON__.api.to_user_ns('users')
        __IPYTHON__.api.to_user_ns('u')
        conn = ldap.get_conn()
        __IPYTHON__.api.to_user_ns('conn')
        print 'Session vars'
        print '------------'
        print 'ldap =', ldap
        print 'conn =', conn
        print 'users =', users
        if u:
            print 'u =', repr(u)

        ipshell()
