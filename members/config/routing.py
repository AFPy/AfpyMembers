"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('/', controller='my', action='index')
    map.connect('/login', controller='utils', action='login')
    map.connect('/register/confirm/{uid}/{key}', controller='register', action='confirm')

    # alias for communication
    map.connect('/carte', controller='maps', action='index')
    map.connect('/courrier', controller='my', action='courrier')
    map.connect('/adhesion', controller='my',
                            action='subscribe_form')
    # ajax stuff
    map.connect('/my/subscribers/{stype}/{letter}', controller='my', action='subscribers')
    map.connect('/my/save_payment/{act}/{uid}/{paymentDate}', controller='my',
                                        action='save_payment', paymentDate=None)

    map.connect('/{controller}')
    map.connect('/{controller}/')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/')
    map.connect('/{controller}/{action}/{id}')

    return map
