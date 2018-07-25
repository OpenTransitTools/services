from pyramid.config import Configurator
from gtfsdb import Database
from ott.utils import object_utils
from ott.utils import db_utils

from ott.utils.svr.pyramid.app_config import AppConfig

import logging
log = logging.getLogger(__file__)


def main(global_config, **config):
    """
    this function is the main entry point for pserve / Pyramid
    it returns a Pyramid WSGI application
    see setup.py entry points + config/*.ini [app:main] ala pserve (e.g., bin/pserve config/development.ini)
    """
    app = AppConfig(**config)
    db = connect(config)

    import views
    app.set_db(db)
    app.config_include_scan(views)

    from ott.otp_client.pyramid import views as otp_views
    app.config_include_scan(otp_views)

    from ott.gtfsdb_realtime.pyramid import views as rt_views
    app.config_include_scan(rt_views)

    return app.make_wsgi_app()


def olconnect(settings):
    u = object_utils.safe_dict_val(settings, 'sqlalchemy.url')
    s = object_utils.safe_dict_val(settings, 'sqlalchemy.schema')
    g = object_utils.safe_dict_val(settings, 'sqlalchemy.is_geospatial', False)
    log.info("Database(url={0}, schema={1}, is_geospatial={2})".format(u, s, g))
    return MyGtfsdb(url=u, schema=s, is_geospatial=g)

ECHO = True
def pyramid_to_gtfsdb_params(settings):
    global ECHO
    u = object_utils.safe_dict_val(settings, 'sqlalchemy.url')
    s = object_utils.safe_dict_val(settings, 'sqlalchemy.schema')
    g = object_utils.safe_dict_val(settings, 'sqlalchemy.is_geospatial', False)
    ECHO = object_utils.safe_dict_val(settings, 'sqlalchemy.echo', False)
    return {'url':u, 'schema':s, 'is_geospatial':g}


def connect(settings):
    # import pdb; pdb.set_trace()
    s = pyramid_to_gtfsdb_params(settings)
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
        db_utils.add_schema(val, self.classes)
        try:
            from ott.gtfsdb_realtime.model.base import Base
            db_utils.add_schema(val, Base.__subclasses__())
        except Exception as e:
            log.warn("gtfsdb_realtime not available when trying to set schema {0}".format(val))

    @url.setter
    def url(self, url):
        log.warn("creating a gtfsdb @ {0}".format(url))
        self._url = url

        # create / config the session
        from zope.sqlalchemy import ZopeTransactionExtension
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker
        self.session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

        ### TODO ^^^ refactor this so we can replace self.session_maker with the Zope junk, etc...

        # create the engine
        from sqlalchemy import create_engine
        self.engine = create_engine(url, echo=ECHO, echo_pool=ECHO)
        self.session.configure(bind=self.engine)
        from gtfsdb.model.base import Base
        Base.metadata.bind = self.engine

        if self.is_sqlite:
            self.engine.connect().connection.connection.text_factory = str
