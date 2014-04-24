import logging
log = logging.getLogger(__file__)

from pyramid.config import Configurator
import ott.utils.object_utils as obj


# database
DB = None


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    #import pdb; pdb.set_trace()
    global DB
    DB = connect(settings)

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

    cfg.add_route('route',         '/route')
    cfg.add_route('routes',        '/routes')
    cfg.add_route('route_stops',   '/route_stops')

    cfg.add_route('stress',        '/stress')


def connect(settings):
    u = obj.safe_dict_val(settings, 'sqlalchemy.url')
    s = obj.safe_dict_val(settings, 'sqlalchemy.schema')
    g = obj.safe_dict_val(settings, 'sqlalchemy.is_spatial', False)
    log.info("Database(url={0}, schema={1}, is_spatial={2})".format(u, s, g))
    return MyGtfsdb(url=u, schema=s, is_spatial=g)


from gtfsdb import Database
class MyGtfsdb(Database):

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        log.warn("creating a gtfsdb @ {0}".format(val))
        self._url = val

        # create / config the session
        from zope.sqlalchemy import ZopeTransactionExtension
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker
        self.session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

        # create the engine
        from sqlalchemy import create_engine
        self.engine = create_engine(val)
        self.session.configure(bind=self.engine)
        from gtfsdb.model.base import Base
        Base.metadata.bind = self.engine

        if self.is_sqlite:
            self.engine.connect().connection.connection.text_factory = str

