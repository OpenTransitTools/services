''' NOTE: this package is used to run server load tests against Pyramid
    Not to be run in production (so remove from views.py when not in use) 
'''

import datetime
import time
import logging
log = logging.getLogger(__file__)

from pyramid.response import Response
from pyramid.view     import view_config
from sqlalchemy.orm.exc import NoResultFound

from ott.otp_client.trip_planner import TripPlanner
from ott.utils import html_utils

from ott.data.dao.headsign_dao import StopHeadsignDao
from ott.data.dao.stop_schedule_dao import StopScheduleDao

from gtfsdb import StopTime

from .app import DB
from .app import CONFIG

def do_view_config(cfg):
    cfg.add_route('stress',          '/stress')
    cfg.add_route('stress_tp',       '/stresstp')
    cfg.add_route('stress_load_db',  '/stressload')
    cfg.add_route('stress_sched_db', '/stresssched')
    cfg.add_route('stress_json',     '/stressjson')

@view_config(route_name='stress', renderer='text/plain', http_cache=0)
def stress(request):
    num = html_utils.get_first_param_as_int(request, 'num', 10)
    out = "wait {0} seconds".format(num)
    time.sleep(num)
    return Response(out, content_type='text/plain')

@view_config(route_name='stress_tp', renderer='text/plain', http_cache=0)
def stress_tp(request):
    otp = html_utils.get_first_param(request, 'svr', "http://localhost/prod")
    out = TripPlanner.call_otp(otp + "?fromPlace=2::45.420597,-122.675674&toPlace=zoo::45.510185,-122.71586&time=12:35pm&maxHours=6&date=2014-5-6&mode=TRANSIT,WALK&optimize=QUICK&maxWalkDistance=1260.0&arriveBy=false")
    return Response(out, content_type='text/plain')

@view_config(route_name='stress_load_db', renderer='text/plain', http_cache=0)
def stress_db_load(request):
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
        out = "Crazy exception {0}".format(e)

    return Response(out, content_type='text/plain')

@view_config(route_name='stress_sched_db', renderer='text/plain', http_cache=0)
def stress_sched_db(request):
    sid = html_utils.get_first_param(request, 'stop_id', "2")
    rid = html_utils.get_first_param(request, 'route_id', None)
    session = DB.session()
    stop_times = StopTime.get_departure_schedule(session=session, stop_id=sid, route_id=rid)
    out = ""
    for st in stop_times:
        if st.is_boarding_stop():
            out = out + st.departure_time + " "
    return Response(out, content_type='text/plain')

@view_config(route_name='stress_json', renderer='json', http_cache=0)
def stress_json(request):
    sid = html_utils.get_first_param(request, 'stop_id', "2")
    rid = html_utils.get_first_param(request, 'route_id', None)
    session = DB.session()
    stop_times = StopTime.get_departure_schedule(session=session, stop_id=sid, route_id=rid)
    out = ""
    json = []
    for i, st in enumerate(stop_times):
        out = out + st.departure_time + " "
        id = StopHeadsignDao.unique_id(st)
        now = datetime.datetime.now()
        time = StopScheduleDao.make_stop_time(st, id, now, i+1)
        json.append(time)
    return Response(json, content_type='text/plain')
