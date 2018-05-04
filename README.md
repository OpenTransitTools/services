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
  1. rm nohup.out; nohup bin/pserve config/development.ini --reload SERVICES=1 &
  2. http://localhost:44444/stop?stop_id=2&full

test:
  0. run the server (see above)
  1. bin/test
  3. bin/geocode PDX  ## run/test the geocoder via the command line
