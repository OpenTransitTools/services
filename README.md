services
========

web services for transit (in python & pyramid)

load gtfs
  0. install python 2.7, along with zc.buildout and easy_install, git
  1. git clone https://github.com/OpenTransitTools/service.git
  2. cd service
  3. buildout
  4. git update-index --assume-unchanged .pydevproject
  5. SQL LITE: bin/gtfsdb-load --database_url sqlite://gtfs.db http://developer.trimet.org/schedule/gtfs.zip
     - or -
     PostGIS: bin/gtfsdb-load --database_url postgresql://postgres@127.0.0.1:5432/postgres --is_geospatial --schema ott http://developer.trimet.org/schedule/gtfs.zip


