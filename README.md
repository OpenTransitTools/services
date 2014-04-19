service
=======

web services for transit (in python & pyramid)

load gtfs
  0. install python 2.7, along with zc.buildout and easy_install, git
  1. git clone https://github.com/OpenTransitTools/service.git
  2. cd service
  3. buildout
  4. git update-index --assume-unchanged .pydevproject
  5. SQL LITE: bin/gtfsdb-load --is_geospatial --schema ott --database_url sqlite://gtfs.db http://developer.trimet.org/schedule/gtfs.zip
     - or -
     PostGIS:  bin/ -c http://developer.trimet.org/schedule/gtfs.zip -s ott -d postgresql://postgres@127.0.0.1:5432/postgres 


