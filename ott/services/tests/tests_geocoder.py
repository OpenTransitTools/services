import unittest
from pyramid import testing

import urllib
import contextlib
import json

from .tests import call_url, get_url

class TestGeoCoder(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_zoo(self):
        url = get_url('geostr', 'place=zoo')
        j = call_url(url)
        s = json.dumps(j)
        self.assertRegexpMatches(s,"-122.71")
        self.assertRegexpMatches(s,"45.51")
