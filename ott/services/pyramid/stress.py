''' NOTE: this package is used to run server load tests against Pyramid
    Not to be run in production (so remove from views.py when not in use) 
'''

import time
import logging
log = logging.getLogger(__file__)

from pyramid.response import Response
from pyramid.view     import view_config
from sqlalchemy.orm.exc import NoResultFound

from ott.otp_client.trip_planner import TripPlanner

from ott.utils import html_utils
 
from .app import DB
from .app import CONFIG

@view_config(route_name='stress', renderer='text/plain', http_cache=0)
def stress(request):
    num = html_utils.get_first_param_as_int(request, 'num', 10)
    out = "wait {0} seconds".format(num)
    time.sleep(num)
    return Response(out, content_type='text/plain')

@view_config(route_name='stress2', renderer='text/plain', http_cache=0)
def stress2(request):
    otp = html_utils.get_first_param(request, 'svr', "http://localhost/prod")
    out = TripPlanner.call_otp(otp + "?fromPlace=2::45.420597,-122.675674&toPlace=zoo::45.510185,-122.71586&time=12:35pm&maxHours=6&date=2014-5-6&mode=TRANSIT,WALK&optimize=QUICK&maxWalkDistance=1260.0&arriveBy=false")
    return Response(out, content_type='text/plain')

@view_config(route_name='stress1', renderer='text/plain', http_cache=0)
def stress1(request):
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

