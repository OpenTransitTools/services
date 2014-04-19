from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

'''
@view_config(route_name='home', renderer='templates/mytemplate.pt')
'''

@view_config(route_name='home', renderer='json')
def my_view(request):
    try:
        #one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
        one = DBSession.query(MyModel).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one.name, 'project': 'test'}

conn_err_msg = """\
Danger. Danger Chris Robson.  Danger.
"""

