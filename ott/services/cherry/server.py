import cherrypy
import logging
log = logging.getLogger(__file__)

from gtfsdb import Database
from ott.services import cpdb

class OttServer(object):
    def __init__(self):
        u = "postgresql+psycopg2://geoserve@maps10.trimet.org:5432/trimet"
        s = "otz"
        g = True
        log.info("Database(url={0}, schema={1}, is_spatial={2})".format(u, s, g))
        #self.db = Database(url=u, schema=s, is_spatial=g)
        self.db = cpdb.MyGtfsdb(url=u, schema=s, is_spatial=g)

    @cherrypy.expose
    #@cherrypy.tools.json_out()
    @cherrypy.tools.response_headers(headers = [
            ('Content-Type', 'text/plain'), 
            ('Cache-Control', 'max-age=0')
    ])
    def index(self, num, poo="warm", **args):
        session = None
        try:
            from ott.data.tests import load_routines
            from ott.utils import html_utils
            from ott.utils import num_utils
            print poo
            num = num_utils.to_int(num, 10)
            session = self.db.get_session()
            out = load_routines.stops(num, session)
            return out
        except Exception, e:
            try:
                session.rollback()
            except:
                pass
        finally:
            try:
                session.rollback()
            except:
                pass
            print "in finally"

cherrypy.config.update('config/server.ini')
cherrypy.quickstart(OttServer())

