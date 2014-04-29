import logging
log = logging.getLogger(__file__)

from pyramid.response import Response
from pyramid.view     import view_config
from sqlalchemy.orm.exc import NoResultFound

from ott.data.dao.base_dao import DatabaseNotFound
from ott.data.dao.base_dao import ServerError
from ott.data.dao.stop_dao import StopDao
from ott.data.dao.stop_dao import StopListDao
from ott.data.dao.route_dao import RouteDao
from ott.data.dao.route_dao import RouteListDao
from ott.data.dao.route_stop_dao import RouteStopDao 

from ott.utils.parse.stop_param_parser import StopParamParser
from ott.utils.parse.geo_param_parser import GeoParamParser
from ott.utils.parse.route_param_parser import RouteParamParser
from ott.data.dao.stop_schedule_dao import StopScheduleDao
from ott.geocoder.geosolr import GeoSolr

from ott.utils import html_utils

from app import DB
from app import CONFIG
SOLR = GeoSolr('http://maps.trimet.org/solr')


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
        session = DB.session()
        rp = RouteParamParser(request)
        r = RouteDao.from_route_id(session, rp.route_id)
        ret_val = json_response(r.to_json())
    except NoResultFound, e:
        log.warn(e)
        ret_val = json_response(data_not_found.to_json(), status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg.to_json(), status=system_err_msg.status_code)
    finally:
        close_session(session)

    return ret_val


@view_config(route_name='routes', renderer='json', http_cache=cache_long)
def routes(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        r = RouteListDao.route_list(session)
        ret_val = json_response(r.to_json())
    except NoResultFound, e:
        log.warn(e)
        ret_val = json_response(data_not_found.to_json(), status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg.to_json(), status=system_err_msg.status_code)
    finally:
        close_session(session)

    return ret_val

@view_config(route_name='route_stops', renderer='json', http_cache=cache_long)
def route_stops(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        sp = StopParamParser(request)
        rs = RouteStopDao.from_route_direction(session, sp.route_id, sp.direction_id)
        ret_val = json_response(rs.to_json())
    except NoResultFound, e:
        log.warn(e)
        ret_val = json_response(data_not_found.to_json(), status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg.to_json(), status=system_err_msg.status_code)
    finally:
        close_session(session)

    return ret_val


@view_config(route_name='stop', renderer='json', http_cache=cache_long)
def stop(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        sp = StopParamParser(request)
        s = StopDao.from_stop_id(session, sp.stop_id)
        ret_val = json_response(s.to_json())
    except NoResultFound, e:
        log.warn(e)
        ret_val = json_response(data_not_found.to_json(), status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg.to_json(), status=system_err_msg.status_code)
    finally:
        close_session(session)

    return ret_val


@view_config(route_name='stops_near', renderer='json', http_cache=cache_long)
def stops_near(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        gp = GeoParamParser(request)
        sl = StopListDao.nearest_stops(session, geo_params=gp)
        ret_val = json_response(sl.to_json())
    except NoResultFound, e:
        log.warn(e)
        ret_val = json_response(data_not_found.to_json(), status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg.to_json(), status=system_err_msg.status_code)
    finally:
        close_session(session)

    return ret_val


@view_config(route_name='stop_schedule', renderer='json', http_cache=cache_short)
def stop_schedule(request):
    ret_val = None
    session = None
    try:
        session = DB.session()
        sp = StopParamParser(request)
        s = StopScheduleDao.get_stop_schedule(session, sp.stop_id)
        ret_val = json_response(s.to_json())
    except NoResultFound, e:
        log.warn(e)
        ret_val = json_response(data_not_found.to_json(), status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg.to_json(), status=system_err_msg.status_code)
    finally:
        close_session(session)

    return ret_val


@view_config(route_name='plan_trip', renderer='json', http_cache=cache_short)
def plan_trip(request):
    ret_val = None
    session = None
    try:
        tp = TripParamParser(request)
        ret_val = json_response(trip.to_json())
    except NoResultFound, e:
        log.warn(e)
        ret_val = json_response(data_not_found.to_json(), status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg.to_json(), status=system_err_msg.status_code)
    finally:
        close_session(session)

    return ret_val


@view_config(route_name='geocode', renderer='json', http_cache=cache_long)
def geocode(request):
    ret_val = None
    try:
        import pdb; pdb.set_trace()
        place = request.params.get('place')
        gc = SOLR.geocode(place)
        ret_val = gc.to_json()
    except NoResultFound, e:
        #TODO ... ^^^^ need SOLR not found 
        log.warn(e)
        ret_val = json_response(data_not_found.to_json(), status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        ret_val = json_response(system_err_msg.to_json(), status=system_err_msg.status_code)
    finally:
        pass

    return ret_val

@view_config(route_name='geostr', renderer='string', http_cache=cache_long)
def geostr(request):
    ret_val = None
    try:
        place = request.params.get('place')
        gc = SOLR.geostr(place)
        ret_val = gc
    except NoResultFound, e:
        #TODO ... ^^^^ need SOLR not found 
        log.warn(e)
        ret_val = json_response(data_not_found.status_message, status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        ret_val = json_response(system_err_msg.status_message, status=system_err_msg.status_code)
    finally:
        pass

    return ret_val


@view_config(route_name='solr', renderer='json', http_cache=cache_long)
def solr(request):
    ret_val = None
    try:
        place = request.params.get('place')
        gc = SOLR.solr(place)
        ret_val = gc
    except NoResultFound, e:
        #TODO ... ^^^^ need SOLR not found 
        log.warn(e)
        ret_val = json_response(data_not_found.to_json(), status=data_not_found.status_code)
    except Exception, e:
        log.warn(e)
        ret_val = json_response(system_err_msg.to_json(), status=system_err_msg.status_code)
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


def json_response(json_data, mime='application/json', status=200):
    ''' @return Response() with content_type of 'application/json' '''
    return Response(json_data, content_type=mime, status_int=status)

def json_response_list(lst, mime='application/json', status=200):
    ''' @return Response() with content_type of 'application/json' '''
    json_data = []
    for l in lst:
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


