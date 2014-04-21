from pyramid.response import Response
from pyramid.view     import view_config

from ott.data.json.response_base import ResponseBase
from ott.data.json.stop_response import StopResponse
from ott.data.json.route_response import RouteListResponse
from ott.utils.parse.stop_param_parser import StopParamParser

from .app import gdb



### cache time - affects how long varnish cache will hold a copy of the data
cache_long=36000  # 10 hours
cache_short=600   # 10 minutes

err_msg = ResponseBase.obj_to_json({'error':'True', 'msg':'System error'})


@view_config(route_name='routes', renderer='json', http_cache=cache_long)
def routes(request):
    try:
        routes = RouteListResponse.route_list(gdb.session)
        return json_response(routes.to_json())
    except:
        return json_response(err_msg, status=500)


@view_config(route_name='stop', renderer='json', http_cache=cache_long)
def stop(request):
    try:
        sp = StopParamParser(request)
        s = StopResponse.from_stop_id(sp.stop_id, gdb.session)
        return json_response(s.to_json())
    except:
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
