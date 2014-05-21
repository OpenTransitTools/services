import logging
log = logging.getLogger(__file__)

from pyramid.config import Configurator
import ott.utils.object_utils as obj

# database
DB = None
CONFIG = None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    #import pdb; pdb.set_trace()
    global CONFIG
    global DB
    CONFIG = settings
    DB = connect(settings)

    cfg = Configurator(settings=settings)
    do_view_config(cfg)
    cfg.scan()
    return cfg.make_wsgi_app()


def do_view_config(cfg):
    ''' adds the views (see below) and static directories to pyramid's config
        TODO: is there a better way to dot this (maybe via an .ini file)
    '''
    #cfg.add_route('index',         '/')

    cfg.add_route('plan_trip',     '/plan_trip')
    cfg.add_route('adverts',       '/adverts')

    cfg.add_route('geocode',       '/geocode')
    cfg.add_route('geostr',        '/geostr')
    cfg.add_route('solr',          '/solr')

    cfg.add_route('stop',          '/stop')
    cfg.add_route('stops_near',    '/stops_near')
    cfg.add_route('stop_schedule', '/stop_schedule')

    cfg.add_route('route',         '/route')
    cfg.add_route('routes',        '/routes')
    cfg.add_route('route_stops',   '/route_stops')

    cfg.add_route('stress',        '/stress')
    cfg.add_route('stress1',       '/stress1')
    cfg.add_route('stress2',       '/stress2')


def olconnect(settings):
    u = obj.safe_dict_val(settings, 'sqlalchemy.url')
    s = obj.safe_dict_val(settings, 'sqlalchemy.schema')
    g = obj.safe_dict_val(settings, 'sqlalchemy.is_geospatial', False)
    log.info("Database(url={0}, schema={1}, is_geospatial={2})".format(u, s, g))
    #import pdb; pdb.set_trace()
    return MyGtfsdb(url=u, schema=s, is_geospatial=g)

def pyramid_to_gtfsdb_params(settings):
    u = obj.safe_dict_val(settings, 'sqlalchemy.url')
    s = obj.safe_dict_val(settings, 'sqlalchemy.schema')
    g = obj.safe_dict_val(settings, 'sqlalchemy.is_geospatial', False)
    return {'url':u, 'schema':s, 'is_geospatial':g}

def connect(settings):
    #import pdb; pdb.set_trace()
    s=pyramid_to_gtfsdb_params(settings)
    log.info("Database({0})".format(s))
    return MyGtfsdb(**s)


from gtfsdb import Database
class MyGtfsdb(Database):

    @property
    def url(self):
        return self._url

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, val):
        self._schema = val
        for cls in self.classes:
            cls.__table__.schema = val

        try:
            from ott.data.gtfsrdb import model
            model.add_schema(val)
        except:
            log.warn("gtfsrdb not available when trying to set schema {0}".format(val))

    @url.setter
    def url(self, url):
        log.warn("creating a gtfsdb @ {0}".format(url))
        self._url = url

        # create / config the session
        from zope.sqlalchemy import ZopeTransactionExtension
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker
        self.session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

        # create the engine
        from sqlalchemy import create_engine
        self.engine = create_engine(url)
        self.session.configure(bind=self.engine)
        from gtfsdb.model.base import Base
        Base.metadata.bind = self.engine

        if self.is_sqlite:
            self.engine.connect().connection.connection.text_factory = str

