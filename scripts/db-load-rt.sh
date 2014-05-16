. ~/services/scripts/db-common.sh

cd $BASEDIR

echo "LOAD GTRTFS ALERTS (from $PWD):"
echo "START > > > > > "
date

echo "bin/load_rt -s $OTT_SCHEMA -1 -c -o -a http://localhost/trimet.org/transweb/ws/V1/FeedSpecAlerts/appId/3819A6A38C72223198B560DF0/includeFuture/true -d postgresql://$PGUSER@localhost:$PGPORT/$PGDBNAME"
bin/load_rt -s $OTT_SCHEMA -1 -c -o -a http://localhost/trimet.org/transweb/ws/V1/FeedSpecAlerts/appId/3819A6A38C72223198B560DF0/includeFuture/true -d postgresql://$PGUSER@localhost:$PGPORT/$PGDBNAME

date
echo "END < < < < < < "
