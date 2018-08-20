from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound

from ott.data.dao import StopDao
from ott.data.dao import StopListDao
from ott.data.dao import RouteDao
from ott.data.dao import RouteListDao
from ott.data.dao import RouteStopListDao 
from ott.data.dao import StopScheduleDao

from ott.geocoder.geosolr import GeoSolr
from ott.geocoder.geo_dao import GeoListDao

from ott.utils.parse.url.stop_param_parser import StopParamParser
from ott.utils.parse.url.geo_param_parser import GeoParamParser
from ott.utils.parse.url.route_param_parser import RouteParamParser

from ott.utils import json_utils

from ott.utils.svr.pyramid import response_utils
from ott.utils.svr.pyramid.globals import *

import logging
log = logging.getLogger(__file__)


APP_CONFIG=None
def set_app_config(app_cfg):
    """
    called set the singleton AppConfig object
    :see ott.utils.svr.pyramid.app_config.AppConfig :
    """
    global APP_CONFIG
    APP_CONFIG = app_cfg


def do_view_config(cfg):
    cfg.add_route('geocode',       '/geocode')
    cfg.add_route('geostr',        '/geostr')
    cfg.add_route('solr',          '/solr')
    cfg.add_route('atis_geocode',  '/atis_geocode')

    cfg.add_route('stop',          '/stop')
    cfg.add_route('stops_near',    '/stops_near')
    cfg.add_route('stop_schedule', '/stop_schedule')
    cfg.add_route('trip_schedule', '/trip_schedule')

    cfg.add_route('route',         '/route')
    cfg.add_route('routes',        '/routes')
    cfg.add_route('route_stops',   '/route_stops')

    cfg.add_route('route_urls',    '/route_urls')
    cfg.add_route('stop_urls',     '/stop_urls')


@view_config(route_name='routes', renderer='json', http_cache=CACHE_LONG)
def routes(request):
    ret_val = None
    session = None
    try:
        session = APP_CONFIG.db.session()
        ret_val = RouteListDao.route_list(session)
    except NoResultFound as e:
        log.warn(e)
        ret_val = DATA_NOT_FOUND_MSG
    except Exception as e:
        log.warn(e)
        rollback_session(session)
        ret_val = SYSTEM_ERROR_MSG
    finally:
        close_session(session)
    return response_utils.dao_response(ret_val)


@view_config(route_name='route', renderer='json', http_cache=CACHE_LONG)
def route(request):
    ret_val = None
    session = None
    try:
        session = APP_CONFIG.db.session()
        rp = RouteParamParser(request)
        ret_val = RouteDao.from_route_id(session, rp.route_id)
    except NoResultFound as e:
        log.warn(e)
        ret_val = DATA_NOT_FOUND_MSG
    except Exception as e:
        log.warn(e)
        rollback_session(session)
        ret_val = SYSTEM_ERROR_MSG
    finally:
        close_session(session)
    return response_utils.dao_response(ret_val)


@view_config(route_name='route_stops', renderer='json', http_cache=CACHE_LONG)
def route_stops(request):
    ret_val = None
    session = None
    try:
        session = APP_CONFIG.db.session()
        params = RouteParamParser(request)
        ret_val = RouteStopListDao.from_params(session, params)
    except NoResultFound as e:
        log.warn(e)
        ret_val = DATA_NOT_FOUND_MSG
    except Exception as e:
        log.warn(e)
        rollback_session(session)
        ret_val = SYSTEM_ERROR_MSG
    finally:
        close_session(session)
    return response_utils.dao_response(ret_val)


@view_config(route_name='stop', renderer='json', http_cache=CACHE_LONG)
def stop(request):
    ret_val = None
    session = None
    try:
        session = APP_CONFIG.db.session()
        params = StopParamParser(request)
        ret_val = StopDao.from_stop_params(session, params)
    except NoResultFound as e:
        log.warn(e)
        ret_val = DATA_NOT_FOUND_MSG
    except Exception as e:
        log.warn(e)
        rollback_session(session)
        ret_val = SYSTEM_ERROR_MSG
    finally:
        close_session(session)
    return response_utils.dao_response(ret_val)


@view_config(route_name='stops_near', renderer='json', http_cache=CACHE_LONG)
def stops_near(request):
    ret_val = None
    session = None
    try:
        session = APP_CONFIG.db.session()
        gp = GeoParamParser(request)
        ret_val = StopListDao.nearest_stops(session, geo_params=gp)
    except NoResultFound as e:
        log.warn(e)
        ret_val = DATA_NOT_FOUND_MSG
    except Exception as e:
        log.warn(e)
        rollback_session(session)
        ret_val = SYSTEM_ERROR_MSG
    finally:
        close_session(session)
    return response_utils.dao_response(ret_val)


@view_config(route_name='stop_schedule', renderer='json', http_cache=CACHE_SHORT)
def stop_schedule(request):
    ret_val = None
    session = None
    try:
        session = APP_CONFIG.db.session()
        sp = StopParamParser(request)
        ret_val = StopScheduleDao.get_stop_schedule_from_params(session, sp)
        if ret_val.stop is None:
            ret_val.has_errors = True
    except NoResultFound as e:
        log.warn(e)
        ret_val = DATA_NOT_FOUND_MSG
    except Exception as e:
        log.warn(e)
        rollback_session(session)
        ret_val = SYSTEM_ERROR_MSG
    finally:
        close_session(session)
    return response_utils.dao_response(ret_val)


@view_config(route_name='trip_schedule', renderer='json', http_cache=CACHE_SHORT)
def trip_schedule(request):
    """
        Trip Schedule:
        http://transitfeeds.com/p/trimet/43/latest/trip/5682380

        List of Trips for Route / Date:
        http://transitfeeds.com/p/trimet/43/latest/route/70/20151202

        http://transitfeeds.com/p/ride-connection/477/latest/route/1998
        http://transitfeeds.com/p/swan-island-evening-shuttle/484/latest/trip/32180A614B2437
    """
    ret_val = None
    session = None
    try:
        from ott.data.dao import TripScheduleDao # TODO
        session = APP_CONFIG.db.session()
        sp = StopParamParser(request)
        ret_val = TripScheduleDao.get_trip_schedule_from_params(session, sp)
    except NoResultFound as e:
        log.warn(e)
        ret_val = DATA_NOT_FOUND_MSG
    except Exception as e:
        log.warn(e)
        rollback_session(session)
        ret_val = SYSTEM_ERROR_MSG
    finally:
        close_session(session)
    return response_utils.dao_response(ret_val)


@view_config(route_name='route_urls', renderer='string', http_cache=CACHE_SHORT)
def route_urls(request):
    """
    return a list of urls based on route ids in the database
    params are 'host' and 'service' ... see how they're used below

    service urls:
        http://localhost:44444/route_urls
        http://localhost:44444/route_urls?host=maps7.trimet.org&service=ride_ws/route_stops
    html pages:
        http://localhost:44444/route_urls?host=maps7.trimet.org&service=ride/stop_select_list.html
    """
    ret_val = ""
    session = None
    try:
        from gtfsdb import Route
        session = APP_CONFIG.db.session()
        routes = Route.active_route_ids(session)
        host = request.params.get('host', request.host)
        service = request.params.get('service', 'route')
        for r in routes:
            url = url_response(host, service, r['route_id'], r['agency_id'])
            ret_val = ret_val + url + "\n"
    except Exception as e:
        log.warn(e)
        rollback_session(session)
        ret_val = SYSTEM_ERROR_MSG.status_message
    finally:
        close_session(session)
    return ret_val


@view_config(route_name='stop_urls', renderer='string', http_cache=CACHE_SHORT)
def stop_urls(request):
    """
    return a list of urls based on stop ids in the database
    params are 'host' and 'service' ... see how they're used below

    service urls:
          http://localhost:44444/stop_urls
          http://localhost:44444/stop_urls?host=maps7.trimet.org&service=ride_ws/stop
          http://localhost:44444/stop_urls?host=maps7.trimet.org&service=ride_ws/stop_schedule
          http://localhost:44444/stop_urls?host=maps7.trimet.org&service=ride_ws/stop_schedule&blocks=t

    html pages:
          http://localhost:44444/stop_urls?host=trimet.org&service=ride/stop.html
          http://localhost:44444/stop_urls?host=trimet.org&service=ride/stop_schedule.html
          http://localhost:44444/stop_urls?host=trimet.org&service=ride/stop_schedule.html&blocks=t
    """
    ret_val = ""
    session = None
    try:
        from gtfsdb import Stop, Block
        limit = request.params.get('limit')
        blocks = request.params.get('blocks')
        host = request.params.get('host', request.host)
        service = request.params.get('service', 'route')
        session = APP_CONFIG.db.session()
        if blocks:
            stops = Block.active_stop_ids(session, limit)
        else:
            stops = Stop.active_stop_ids(session, limit)
        for r in stops:
            url = url_response(host, service, r['stop_id'])
            ret_val = ret_val + url + "\n"
    except Exception as e:
        log.warn(e)
        rollback_session(session)
        ret_val = SYSTEM_ERROR_MSG.status_message
    finally:
        close_session(session)
    return ret_val


def url_response(host, service, id, agency_id=None, extra="&detailed"):
    """
    return a url with id and other good stuff
    """
    url = "http://{}/{}?id={}"
    if agency_id:
        url = "{}&agency_id={}".format(url, agency_id)
    if extra:
        url = url + extra
    ret_val = url.format(host, service, id)
    return ret_val


def rollback_session(session):
    """ rollback session """
    if session:
        try:
            session.rollback()
        except Exception as e:
            log.info('ROLLBACK SESSION {0}'.format(e))
            pass


def close_session(session):
    """
    close session
    NOTE: Pyramid TM is doing the closing for us
    """
    return


#
# TODO: move these to another project, or app...
#

@view_config(route_name='geocode', renderer='json', http_cache=CACHE_LONG)
def geocode(request):
    ret_val = None
    try:
        place = request.params.get('place')
        ret_val = get_solr().geocode(place)
    except IndexError as e:
        log.warn(e)
        ret_val = DATA_NOT_FOUND_MSG
    except Exception as e:
        log.warn(e)
        ret_val = SYSTEM_ERROR_MSG
    finally:
        pass
    return response_utils.dao_response(ret_val)


@view_config(route_name='atis_geocode', renderer='json', http_cache=CACHE_LONG)
def atis_geocode(request):
    ret_val = None
    try:
        url = APP_CONFIG.ini_settings.get('atis_url')
        qs  = request.query_string
        doc = json_utils.stream_json(url, qs)
        ret_val = GeoListDao.make_geo_list_dao(doc)
    except IndexError as e:
        log.warn(e)
        ret_val = DATA_NOT_FOUND_MSG
    except Exception as e:
        log.warn(e)
        ret_val = SYSTEM_ERROR_MSG
    finally:
        pass
    return response_utils.dao_response(ret_val)


@view_config(route_name='geostr', renderer='string', http_cache=CACHE_LONG)
def geostr(request):
    ret_val = None
    try:
        place = request.params.get('place')
        ret_val = get_solr().geostr(place)
    except Exception as e:
        log.warn(e)
        ret_val = SYSTEM_ERROR_MSG.status_message
    finally:
        pass
    return ret_val


@view_config(route_name='solr', renderer='json', http_cache=CACHE_LONG)
def solr(request):
    ret_val = None
    try:
        place = request.params.get('place')
        rows = request.params.get('rows')
        s = get_solr().solr(place, rows)
        ret_val = s
    except IndexError as e:
        log.warn(e)
        ret_val = response_utils.data_not_found_response()
    except Exception as e:
        log.warn(e)
        ret_val = response_utils.sys_error_response()
    finally:
        pass
    return ret_val


SOLR = None
def get_solr():
    # import pdb; pdb.set_trace()
    global SOLR
    if SOLR is None:
        SOLR = GeoSolr(APP_CONFIG.ini_settings.get('solr_url'))
    return SOLR


