export BASEDIR=${HOME}/services
export PYTHON=${BASEDIR}/bin/python
export PATH="${PYTHON}:${BASEDIR}/py/bin/:~/install/jdk/bin:/home/geoserve/postgres/bin/:$PATH"
export LD_LIBRARY_PATH="${BASEDIR}/bin:/home/geoserve/install/postgres/lib:/home/geoserve/install/gdal/lib:/home/geoserve/install/geos/lib"
export OTT_DUMP=ott.tar
export OTT_MIN_SIZE=10000000
export OTT_DUMPER=$BASEDIR/bin/db-dump.sh

function mk_env()
{
    # environment with ott schema
    export MASTER=${MASTER:="geoserve"}
    export PGDBNAME=${PGDBNAME:="trimet"}
    export PGUSER=${PGUSER:="geoserve"}
    export PGPASS=${PGPASS:="YOUR PASSWORD HERE"}
    export PGPORT=${PGPORT:="5432"}
    export PGSCHEMA=${PGSCHEMA:="ott"}
    export OTT_SCHEMA=${OTT_SCHEMA:="ott"}
}

function grantor()
{
    schema=$PGSCHEMA
    if [ $1 ]
    then
        schema=$1
    fi

    if [ $schema != "public" ]
    then
        echo "grant all on schema $schema to $PGUSER;" | psql $PGDBNAME -U $MASTER
        echo "grant all on schema $schema to $MASTER;" | psql $PGDBNAME -U $MASTER
        echo "grant all on schema $schema to tmpublic;"| psql $PGDBNAME -U $MASTER
    fi

    for table in `echo "SELECT relname FROM pg_stat_all_tables where schemaname like '%${schema}%';" | psql $PGDBNAME | grep -v "pg_" | grep "^ "`;
    do
	echo "GRANT ALL ON TABLE ${schema}.$table"
	echo "GRANT ALL ON TABLE ${schema}.$table to $PGUSER;"  | psql $PGDBNAME -U $MASTER
	echo "GRANT ALL ON TABLE ${schema}.$table to $MASTER;"  | psql $PGDBNAME -U $MASTER
	echo "GRANT ALL ON TABLE ${schema}.$table to tmpublic;" | psql $PGDBNAME -U $MASTER
    done
}

# runs a .sql file, but first sets schema to our schema
function run_sql_file()
{
    echo "SET search_path TO $PGSCHEMA,public; \i $1;  | psql $PGDBNAME -U $PGUSER "
    echo "SET search_path TO $PGSCHEMA,public; \i $1;" | psql $PGDBNAME -U $PGUSER
}


mk_env;
