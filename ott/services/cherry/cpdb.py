import logging
log = logging.getLogger(__file__)

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
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker
        self.session = scoped_session(sessionmaker())

        # create the engine
        from sqlalchemy import create_engine
        self.engine = create_engine(val, pool_recycle=60, pool_size=50, max_overflow=50)
        self.session.configure(autoflush=True, bind=self.engine)
        from gtfsdb.model.base import Base
        Base.metadata.bind = self.engine

        if self.is_sqlite:
            self.engine.connect().connection.connection.text_factory = str

    def get_session(self):
        return self.session()
