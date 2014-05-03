import logging
log = logging.getLogger(__file__)

from pyramid.response import Response
from pyramid.view     import view_config
from sqlalchemy.orm.exc import NoResultFound

from ott.data.dao import DatabaseNotFound
from ott.data.dao import ServerError
from ott.data.dao import StopDao
from ott.data.dao import StopListDao
from ott.data.dao import RouteDao
from ott.data.dao import RouteListDao
from ott.data.dao import RouteStopDao 
from ott.data.dao import StopScheduleDao

from ott.utils.parse import StopParamParser
from ott.utils.parse import GeoParamParser
from ott.utils.parse import RouteParamParser

from ott.geocoder.geosolr import GeoSolr
from ott.otp_client.trip_planner import TripPlanner

from ott.utils import html_utils

from app import DB
from app import CONFIG

### cache time - affects how long varnish cache will hold a copy of the data
cache_long=36000  # 10 hours
cache_short=600   # 10 minutes

system_err_msg = ServerError()
data_not_found = DatabaseNotFound()


@view_config(route_name='route', renderer='json', http_cache=cache_long)
def route(request):
    ret_val = None
    session = None
    try:
        #import pdb; pdb.set_trace()
        session = DB.session()
        rp = RouteParamParser(request)
        ret_val = RouteDao.from_route_id(session, rp.route_id)
    except NoResultFound, e:
        log.warn(e)
        ret_val = data_not_found
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = system_err_msg
    finally:
        close_session(session)

    return dao_response(ret_val)


@view_config(route_name='routes', renderer='json', http_cache=cache_long)
def routes(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        ret_val = RouteListDao.route_list(session)
    except NoResultFound, e:
        log.warn(e)
        ret_val = data_not_found
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = system_err_msg
    finally:
        close_session(session)

    return dao_response(ret_val)


@view_config(route_name='route_stops', renderer='json', http_cache=cache_long)
def route_stops(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        sp = StopParamParser(request)
        ret_val = RouteStopDao.from_route_direction(session, sp.route_id, sp.direction_id)
    except NoResultFound, e:
        log.warn(e)
        ret_val = data_not_found
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = system_err_msg
    finally:
        close_session(session)

    return dao_response(ret_val)


@view_config(route_name='stop', renderer='json', http_cache=cache_long)
def stop(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        sp = StopParamParser(request)
        ret_val = StopDao.from_stop_id(session, sp.stop_id)
    except NoResultFound, e:
        log.warn(e)
        ret_val = data_not_found
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = system_err_msg
    finally:
        close_session(session)

    return dao_response(ret_val)


@view_config(route_name='stops_near', renderer='json', http_cache=cache_long)
def stops_near(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        gp = GeoParamParser(request)
        ret_val = StopListDao.nearest_stops(session, geo_params=gp)
    except NoResultFound, e:
        log.warn(e)
        ret_val = data_not_found
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = system_err_msg
    finally:
        close_session(session)

    return dao_response(ret_val)


@view_config(route_name='stop_schedule', renderer='json', http_cache=cache_short)
def stop_schedule(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        sp = StopParamParser(request)
        ret_val = StopScheduleDao.get_stop_schedule(session, sp.stop_id)
    except NoResultFound, e:
        log.warn(e)
        ret_val = data_not_found
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = system_err_msg
    finally:
        close_session(session)

    return dao_response(ret_val)


@view_config(route_name='plan_trip', renderer='json', http_cache=cache_short)
def plan_trip(request):
    ret_val = None
    try:
        #import pdb; pdb.set_trace()
        trip = get_planner().plan_trip(request)
        ret_val = json_response(trip)
    except NoResultFound, e:
        log.warn(e)
        ret_val = dao_response(data_not_found)
    except Exception, e:
        log.warn(e)
        ret_val = dao_response(system_err_msg)
    finally:
        pass

    return ret_val


@view_config(route_name='geocode', renderer='json', http_cache=cache_long)
def geocode(request):
    ret_val = None
    try:
        place = request.params.get('place')
        ret_val = get_solr().geocode(place)
    except IndexError, e:
        log.warn(e)
        ret_val = data_not_found
    except Exception, e:
        log.warn(e)
        ret_val = system_err_msg
    finally:
        pass

    return dao_response(ret_val)


@view_config(route_name='geostr', renderer='string', http_cache=cache_long)
def geostr(request):
    ret_val = None
    try:
        place = request.params.get('place')
        ret_val = get_solr().geostr(place)
    except Exception, e:
        log.warn(e)
        ret_val = system_err_msg.status_message
    finally:
        pass

    return ret_val


@view_config(route_name='solr', renderer='json', http_cache=cache_long)
def solr(request):
    ret_val = None
    try:
        place = request.params.get('place')
        rows  = request.params.get('rows')
        s = get_solr().solr(place, rows)
        ret_val = s
    except IndexError, e:
        log.warn(e)
        ret_val = dao_response(data_not_found)
    except Exception, e:
        log.warn(e)
        ret_val = dao_response(system_err_msg)
    finally:
        pass

    return ret_val


@view_config(route_name='stress', renderer='text/plain', http_cache=0)
def stress(request):
    out = None
    session = None
    try:
        from ott.data.tests import load_routines
        session = DB.session()
        num = html_utils.get_first_param_as_int(request, 'num', 300)
        out = load_routines.stops(num, session)
    except NoResultFound, e:
        log.warn(e)
        out = "Nothing found..."
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        out = "Crazy exception {0}".format(e)
    finally:
        close_session(session)

    return Response(out, content_type='text/plain')


def dao_response(dao):
    ''' using a BaseDao object, send the data to a pyramid Reponse '''
    if dao is None:
        dao = data_not_found
    return json_response(json_data=dao.to_json(), status=dao.status_code)

def json_response(json_data, mime='application/json', status=200):
    ''' @return Response() with content_type of 'application/json' '''
    if json_data is None:
        json_data = data_not_found.to_json()
    return Response(json_data, content_type=mime, status_int=status)

def json_response_list(lst, mime='application/json', status=200):
    ''' @return Response() with content_type of 'application/json' '''
    json_data = []
    for l in lst:
        if l:
            jd = l.to_json()
            json_data.append(jd)
    return json_response(json_data, mime, status)

def rollback_session(session):
    ''' rollback session '''
    if session:
        try:
            session.rollback()
        except Exception, e:
            log.info('ROLLBACK SESSION {0}'.format(e))
            pass

def close_session(session):
    ''' close session '''
    return # NOTE: Pyramid TM is doing the closing for us
    if session:
        try:
            session.commit()
            session.flush()
            session.close()
        except Exception, e:
            log.info('CLOSE SESSION {0}'.format(e))
            pass


SOLR = None
def get_solr():
    global SOLR
    if SOLR is None:
        SOLR = GeoSolr(CONFIG.get('solr_url'))
    return SOLR

TRIP_PLANNER = None
def get_planner():
    global TRIP_PLANNER 
    if TRIP_PLANNER is None:
        otp_url = CONFIG.get('otp_url')
        advert_url = CONFIG.get('advert_url')
        TRIP_PLANNER = TripPlanner(otp_url=otp_url, advert_url=advert_url, solr_instance=get_solr())
    return TRIP_PLANNER



