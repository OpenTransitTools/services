import logging
log = logging.getLogger(__file__)

from pyramid.view import view_config
from ott.utils import html_utils
 
from app import DB
from app import CONFIG

from gtfsdb import Stop


def do_view_config(cfg):
    cfg.add_route('urls', '/urls')


@view_config(route_name='urls', renderer='string', http_cache=0)
def urls(request):
    ret_val = ""

    verbose = html_utils.get_first_param_as_boolean(request, 'verbose', True)
    detailed = html_utils.get_first_param_as_boolean(request, 'detailed', False)
    alerts = html_utils.get_first_param_as_boolean(request, 'alerts', False)
    type = html_utils.get_first_param(request, 'type', 'r:rs:s:sch:ns:')

    extra = ""
    if detailed:
        extra += "detailed" 
    if alerts and detailed:
        extra += "&alerts"
    elif alerts:
        extra += "alerts"

    if verbose:
        ret_val = "{0}&type={1}&verbose={1}\n".format(extra, type, verbose)

    if 'r:' in type:
        ret_val += '{0}/routes?{1}\n'.format(request.host, extra)

    if 'rs:' in type:
        rid = html_utils.get_first_param(request, 'route_id', '100')
        ret_val += '{0}/route_stops?route_id={1}&{2}\n'.format(request.host, rid, extra)

    if 'as:' in type:
        q = DB.session().query(Stop)
        stops = q.all()
        for s in stops:
            ret_val += '{0}/stop?stop_id={1}&{2}\n'.format(request.host, s.stop_id, extra)
    elif 's:' in type:
        sid = html_utils.get_first_param(request, 'stop_id', '2')
        ret_val += '{0}/stop?stop_id={1}&{2}\n'.format(request.host, sid, extra)

    if 'asch:' in type:
        q = DB.session().query(Stop)
        stops = q.all()
        for s in stops:
            ret_val += '{0}/stop_schedule?stop_id={1}&{2}\n'.format(request.host, s.stop_id, extra)
    elif 'sch:' in type:
        sid = html_utils.get_first_param(request, 'stop_id', '2')
        ret_val += '{0}/stop_schedule?stop_id={1}&{2}\n'.format(request.host, sid, extra)

    if 'ns:' in type:
        lat = html_utils.get_first_param_as_float(request, 'lat', '45.555')
        lon = html_utils.get_first_param_as_float(request, 'lon', '-122.5')
        ret_val += '{0}/stops_near?lat={1}&lon={2}&{3}\n'.format(request.host, lat, lon, extra)

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
