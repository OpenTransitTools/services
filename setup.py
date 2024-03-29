import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'ott.utils',
    'ott.geocoder',
    'ott.otp_client',
    'ott.data[postgresql]',

    'gtfsdb',
    'zope.sqlalchemy',

    'venusian==1.2.0',
    'waitress==1.4.3',
    'pyramid',
    'pyramid_tm',
    'pyramid_exclog',
]

extras_require = dict(
    dev=[
      '' if os.name == 'nt' or os.name == 'posix' else 'linesman'
    ],
)

setup(
    name='ott.services',
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

    dependency_links = [
        'git+https://github.com/OpenTransitTools/otp_client_py.git#egg=ott.otp_client-0.1.0',
        'git+https://github.com/OpenTransitTools/geocoder.git#egg=ott.geocoder-0.1.0',
        'git+https://github.com/OpenTransitTools/utils.git#egg=ott.utils-0.1.0',
        'git+https://github.com/OpenTransitTools/data.git#egg=ott.data-0.1.0',
        'git+https://github.com/OpenTransitTools/gtfsdb.git#egg=gtfsdb-0.1.7',
    ],

    license="Mozilla-derived (http://opentransittools.com)",
    url='http://opentransittools.com',
    keywords='ott, otp, services, transit',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=extras_require,
    tests_require=requires,
    test_suite="ott.services.tests",
    entry_points="""\
        [paste.app_factory]
        main = ott.services.pyramid.app:main
    """,
)
