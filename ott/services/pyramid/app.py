from pyramid.config import Configurator
import ott.utils.object_utils as obj
from gtfsdb import Database
import logging
log = logging.getLogger(__file__)


# database
DB = None
CONFIG = None
ECHO = True


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # logging config for pserve / wsgi
    if settings and 'logging_config_file' in settings:
        from pyramid.paster import setup_logging
        setup_logging(settings['logging_config_file'])

    # import pdb; pdb.set_trace()
    global CONFIG
    global DB
    CONFIG = settings
    DB = connect(settings)

    import views
    config.include(views.do_view_config)
    config.scan('ott.services.pyramid')

    return config.make_wsgi_app()


def olconnect(settings):
    u = obj.safe_dict_val(settings, 'sqlalchemy.url')
    s = obj.safe_dict_val(settings, 'sqlalchemy.schema')
    g = obj.safe_dict_val(settings, 'sqlalchemy.is_geospatial', False)
    log.info("Database(url={0}, schema={1}, is_geospatial={2})".format(u, s, g))
    return MyGtfsdb(url=u, schema=s, is_geospatial=g)


def pyramid_to_gtfsdb_params(settings):
    global ECHO
    u = obj.safe_dict_val(settings, 'sqlalchemy.url')
    s = obj.safe_dict_val(settings, 'sqlalchemy.schema')
    g = obj.safe_dict_val(settings, 'sqlalchemy.is_geospatial', False)
    ECHO = obj.safe_dict_val(settings, 'sqlalchemy.echo', False)
    return {'url':u, 'schema':s, 'is_geospatial':g}


def connect(settings):
    # import pdb; pdb.set_trace()
    s=pyramid_to_gtfsdb_params(settings)
    log.info("Database({0})".format(s))
    return MyGtfsdb(**s)


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
        self.engine = create_engine(url, echo=ECHO, echo_pool=ECHO)
        self.session.configure(bind=self.engine)
        from gtfsdb.model.base import Base
        Base.metadata.bind = self.engine

        if self.is_sqlite:
            self.engine.connect().connection.connection.text_factory = str
