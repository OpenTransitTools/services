import logging
log = logging.getLogger(__file__)

from pyramid.response import Response
from pyramid.view     import view_config
from sqlalchemy.orm.exc import NoResultFound

from ott.data.dao.base_dao import BaseDao
from ott.data.dao.stop_dao import StopDao
from ott.data.dao.route_dao import RouteDao
from ott.data.dao.route_dao import RouteListDao
from ott.data.dao.route_stop_dao import RouteStopDao 

from ott.utils.parse.stop_param_parser import StopParamParser
from ott.utils.parse.route_param_parser import RouteParamParser
from ott.utils import html_utils

from app import DB


### cache time - affects how long varnish cache will hold a copy of the data
cache_long=36000  # 10 hours
cache_short=600   # 10 minutes

system_err_msg = BaseDao.obj_to_json({'error':'True', 'msg':'System error'})
data_not_found = BaseDao.obj_to_json({'error':'True', 'msg':'Data not found'})


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
        ret_val = json_response(data_not_found, status=500)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg, status=500)
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
        ret_val = json_response(data_not_found, status=500)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg, status=500)
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
        ret_val = json_response(data_not_found, status=500)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg, status=500)
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
        ret_val = json_response(data_not_found, status=500)
    except Exception, e:
        log.warn(e)
        rollback_session(session)
        ret_val = json_response(system_err_msg, status=500)
    finally:
        close_session(session)

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
    if session:
        try:
            session.commit()
            session.flush()
            session.close()
        except Exception, e:
            log.info('CLOSE SESSION {0}'.format(e))
            pass


