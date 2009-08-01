# -*- coding: utf-8 -*-
from afpy.ldap import custom as ldap
from authkit.permissions import *
from decorator import decorator
from pylons import request

def authorize(permission):
    """
    This is a decorator which can be used to decorate a Pylons controller action.
    It takes the permission to check as the only argument and can be used with
    all types of permission objects.
    """
    def validate(func, self, *args, **kwargs):
        def app(environ, start_response):
            return func(self, *args, **kwargs)
        return permission.check(app, request.environ, self.start_response)
    return decorator(validate)


class AdminUsers(UserIn):
    def check(self, app, environ, start_response):
        if 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated')
        if environ['REMOTE_USER'].lower() not in self.users:
            raise NotAuthorizedError('You are not one of the users allowed to access this resource.')
        return app(environ, start_response)

AdminUser = AdminUsers([u.lower() for u in ldap.getMembersOf('bureau')])
AfpyUser = RemoteUser()

#AdminUser = UserIn(['toto'])

