import logging
log = logging.getLogger(__file__)

from pyramid.response import Response
from pyramid.view     import view_config

from ott.data.dao.base_dao import BaseDao
from ott.data.dao.stop_dao import StopDao
from ott.data.dao.route_dao import RouteDao
from ott.data.dao.route_dao import RouteListDao

from ott.utils.parse.stop_param_parser import StopParamParser
from ott.utils.parse.route_param_parser import RouteParamParser

from app import DB


### cache time - affects how long varnish cache will hold a copy of the data
cache_long=36000  # 10 hours
cache_short=600   # 10 minutes

err_msg = BaseDao.obj_to_json({'error':'True', 'msg':'System error'})


@view_config(route_name='route', renderer='json', http_cache=cache_long)
def route(request):
    try:
        rp = RouteParamParser(request)
        r = RouteDao.from_route_id(rp.route_id, DB.session)
        return json_response(r.to_json())
    except Exception, e:
        log.warn(e)
        return json_response(err_msg, status=500)

@view_config(route_name='routes', renderer='json', http_cache=cache_long)
def routes(request):
    try:
        r = RouteListDao.route_list(DB.session)
        return json_response(r.to_json())
    except Exception, e:
        log.warn(e)
        return json_response(err_msg, status=500)


@view_config(route_name='stop', renderer='json', http_cache=cache_long)
def stop(request):
    try:
        sp = StopParamParser(request)
        s = StopDao.from_stop_id(sp.stop_id, DB.session)
        return json_response(s.to_json())
    except Exception, e:
        log.warn(e)
        return json_response(err_msg, status=500)


def json_response(json_data, mime='application/json', status=200):
    ''' @return Response() with content_type of 'application/json' '''
    return Response(json_data, content_type=mime, status_int=status)

def json_response_list(list, mime='application/json', status=200):
    ''' @return Response() with content_type of 'application/json' '''
    json_data = []
    for l in list:
        jd = l.to_json()
        json_data.append(jd)
    return json_response(json_data, mime, status)
