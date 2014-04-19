import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_beaker',
    'waitress',
    'sqlalchemy<0.9.0',
    'geoalchemy',
    'zope.sqlalchemy',
    'pyramid_tm',
    'transaction',
    #'gtfsdb',
    'psycopg2',
    'simplejson',
]

extras_require = dict(
    dev=[],
    geo=['geoalchemy>=0.6'],
    oracle=['cx_oracle>=5.1'],
    postgresql=['psycopg2>=2.4.2'],
)

#
# eggs that you need if you're running a version of python lower than 2.7
#
if sys.version_info[:2] < (2, 7):
    requires.extend(['argparse>=1.2.1', 'unittest2>=0.5.1'])


setup(
    name='ott.service',
    version='0.1.0',
    description='Open Transit Tools - Web API / Controller',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Open Transit Tools",
    author_email="info@opentransittools.org",
    dependency_links=('http://opentransittools.com',),
    license="Mozilla-derived (http://opentransittools.com)",
    url='http://opentransittools.com',
    keywords='ott, otp, services, transit',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=requires,
    test_suite="ott.service.tests",
    entry_points="""\
        [paste.app_factory]
        main = ott.service.app:main
        [console_scripts]
        initialize_test_db = ott.service.scripts.initializedb:main
    """,
        #initialize_test_db = test.scripts.initializedb:main
        #main = ott.service.pyramid.app:main
)
