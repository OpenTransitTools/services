from pyramid.config import Configurator
from gtfsdb import Database

# database
gdb = None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    global gdb
    gdb = Database(url="sqlite:///gtfs.db")
    config = Configurator(settings=settings)
    do_view_config(config)
    config.scan()
    return config.make_wsgi_app()


def do_view_config(cfg):
    ''' adds the views (see below) and static directories to pyramid's config
        TODO: is there a better way to dot this (maybe via an .ini file)
    '''
    #cfg.add_route('index',         '/')
    #cfg.add_route('plan_trip',     '/plan_trip')
    #cfg.add_route('adverts',       '/adverts')

    #cfg.add_route('geocode',       '/geocode')
    #cfg.add_route('geostr',        '/geostr')
    #cfg.add_route('solr',          '/solr')

    cfg.add_route('stop',          '/stop')
    #cfg.add_route('stop_schedule', '/stop_schedule')
    #cfg.add_route('stops_near',    '/stops_near')

    cfg.add_route('routes',        '/routes')
    #cfg.add_route('route_stops',   '/route_stops')


