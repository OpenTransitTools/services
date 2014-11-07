import unittest
import json
import urllib

from ott.utils.parse import csv_reader
from .tests import call_url, get_url

class TestGeoCoder(unittest.TestCase):
    def setUp(self):
        here = csv_reader.Csv.get_dirname(__file__)
        self.csv_file = csv_reader.Csv('geocodes.csv', here)
        self.test_data = self.csv_file.open()

    def tearDown(self):
        self.csv_file.close()
        pass

    def test_zoo(self):
        url = get_url('geostr', 'place=zoo')
        j = call_url(url)
        s = json.dumps(j)
        self.assertRegexpMatches(s,"-122.71")
        self.assertRegexpMatches(s,"45.51")


    def test_geocode_csv_data(self):
        for d in self.test_data:
            u = "http://dev.trimet.org/ride_ws/geostr?place={0}".format(d['name'])
            s = urllib.urlopen(u) 
            print d, u, s
            self.assertRegexpMatches(s,d['lat'])
            self.assertRegexpMatches(s,d['lon'])
