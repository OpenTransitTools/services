import logging
log = logging.getLogger(__file__)

from ott.utils import html_utils
 
from app import DB
from app import CONFIG

def do_view_config(cfg):
    cfg.add_route('urls', '/urls')

@view_config(route_name='urls', renderer='text', http_cache=0)
def urls(request):
    ret_val = None
    v = html_utils.RouteParamParser(request)
    return ret_val


def blah(request):
    ret_val = None
    session = None
    try:
        #import pdb; pdb.set_trace()
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
