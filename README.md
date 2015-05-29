services
========

Services API for ott.view (gtfs / trasnit web service)
@see http://opentransittools.com/view

build:
  0. install python 2.7, along easy_install, zc.buildout ("zc.buildout==1.5.2") and git
  1. git clone https://github.com/OpenTransitTools/services.git
  2. cd services
  3. buildout
  4. git update-index --assume-unchanged .pydevproject

run:
  1. rm nohup.out; nohup bin/pserve config/pc.ini --reload SERVICES=1 &
  2. http://localhost:44444/stop?stop_id=2&full

test:
  0. run the server (see above)
  1. bin/test
  3. bin/geocode PDX  ## run/test the geocoder via the command line


load gtfs
  0. install python 2.7, along with zc.buildout and easy_install, git
  1. git clone https://github.com/OpenTransitTools/service.git
  2. cd service
  3. buildout
  4. git update-index --assume-unchanged .pydevproject
  5. SQL LITE: bin/gtfsdb-load --database_url sqlite://gtfs.db http://developer.trimet.org/schedule/gtfs.zip
     - or -
     PostGIS: bin/gtfsdb-load --database_url postgresql://postgres@127.0.0.1:5432/postgres --is_geospatial --schema ott http://developer.trimet.org/schedule/gtfs.zip


