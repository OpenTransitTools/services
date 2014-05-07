import cherrypy
import logging
log = logging.getLogger(__file__)

from ott.geocoder.geosolr import GeoSolr
from ott.otp_client.trip_planner import TripPlanner
from ott.utils import html_utils

class OttServer(object):
    def __init__(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def plan_trip(self, **args):
        ret_val = None
        try:
            #import pdb; pdb.set_trace()
            trip = get_planner().plan_trip(args)
            ret_val = trip
        except Exception, e:
            log.warn(e)
            ret_val = {'e':'error'}
            '''
            except NoResultFound, e:
                log.warn(e)
                ret_val = dao_response(data_not_found)
            except Exception, e:
                log.warn(e)
                ret_val = dao_response(system_err_msg)
            '''
        finally:
            pass
        return ret_val

SOLR = None
def get_solr():
    global SOLR
    if SOLR is None:
        SOLR = GeoSolr("http://maps10.trimet.org/solr")
    return SOLR

TRIP_PLANNER = None
def get_planner():
    global TRIP_PLANNER 
    if TRIP_PLANNER is None:
        otp_url = "http://maps10.trimet.org/prod"
        advert_url = "http://trimet.org/map/adverts"
        TRIP_PLANNER = TripPlanner(otp_url=otp_url, advert_url=advert_url, solr_instance=get_solr())
    return TRIP_PLANNER

cherrypy.config.update('config/production.ini')
cherrypy.quickstart(OttServer())
