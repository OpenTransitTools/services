import os
import sys
import setuptools
from setuptools import setup, find_packages
setuptools.dist.Distribution(dict(setup_requires='Babel')) # for message_extractors line below (else warnings / errors)

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
    'gtfsdb',
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

setup(name='test',
      version='0.0',
      description='test',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='test',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = test:main
      [console_scripts]
      initialize_test_db = test.scripts.initializedb:main
      """,
      )

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
    keywords='ott, otp, controller, transit',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    install_requires=requires,
    extras_require=extras_require,
    tests_require=requires,
    test_suite="ott.controller",
    entry_points="""\
        [paste.app_factory]
        main = test:main
        [console_scripts]
        initialize_test_db = test.scripts.initializedb:main
    """,
        #main = ott.service.pyramid.app:main
)
