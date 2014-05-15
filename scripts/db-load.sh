. ~/services/scripts/db-common.sh

cd $BASEDIR

echo "START > > > > > "
date

# move the current ott schema
drop_schema;
create_schema;

bin/gtfsdb-load --database_url postgresql://$PGUSER@localhost:$PGPORT/$PGDBNAME -s $OTT_SCHEMA --is_geospatial $GTFS_ZIP

date
echo "END < < < < < < "
