from pyramid.response import Response
from pyramid.view     import view_config

from ott.data.json.stop_response import StopResponse
from .app import gdb


@view_config(route_name='home', renderer='json')
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
"""

