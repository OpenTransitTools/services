from pyramid.response import Response
from pyramid.view     import view_config

from ott.data.json.stop_response import StopResponse
from ott.data.json.route_response import RouteListResponse
from ott.utils.parse.stop_param_parser import StopParamParser

from .app import gdb


###
### cache time
###
cache_long=36000  # 10 hours
cache_short=600   # 10 minutes


@view_config(route_name='routes', renderer='json', http_cache=cache_long)
def routes(request):
    routes = RouteListResponse.route_list(gdb.session)
    ret_val = routes.to_json()
    return json_response(ret_val)

@view_config(route_name='stop', renderer='json', http_cache=cache_long)
def stop(request):
    sp = StopParamParser(request)
    s = StopResponse.from_stop_id(sp.stop_id, gdb.session)
    ret_val = s.to_json()
    return json_response(ret_val)

#@view_config(route_name='home', renderer='json')
def my_view(request):
    '''
    '''
    ret_val = None
    
    try:
        s = StopResponse.from_stop_id('2', gdb.session)
        ret_val = s.to_json()
    except:
        ret_val = Response(conn_err_msg, content_type='text/plain', status_int=500)
    return ret_val

conn_err_msg = """\
Danger. Danger Chris Robson.  Danger.
TURN ME INTO JSON 
"""


def json_response(json_data, mime='application/json'):
    ''' @return Response() with content_type of 'application/json' '''
    return Response(json_data, content_type=mime)

def json_response_list(list, mime='application/json'):
    ''' @return Response() with content_type of 'application/json' '''
    json_data = []
    for l in list:
        jd = l.to_json()
        json_data.append(jd)
        #json_data = jd
    return Response(json_data, content_type=mime)

