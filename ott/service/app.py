from pyramid.config import Configurator
from gtfsdb import Database

gdb = None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    global gdb
    gdb = Database(url="sqlite:///gtfs.db")
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
