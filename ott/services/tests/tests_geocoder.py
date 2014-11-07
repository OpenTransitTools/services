import unittest
import json

from ott.utils.parse import csv_reader
from .tests import call_url, get_url

class TestGeoCoder(unittest.TestCase):
    def setUp(self):
        here = csv_reader.Csv.get_dirname(__file__)
        c = csv_reader.Csv('geocodes.csv', here)
        self.test_data = c.open()
        c.close()

    def tearDown(self):
        pass

    def test_zoo(self):
        url = get_url('geostr', 'place=zoo')
        j = call_url(url)
        s = json.dumps(j)
        self.assertRegexpMatches(s,"-122.71")
        self.assertRegexpMatches(s,"45.51")
