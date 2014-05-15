. ~/services/scripts/db-common.sh

cd $BASEDIR

echo "START > > > > > "
date

# check to see the size of the dump and load it if there
size=`ls -Hltr ${OTT_DUMP}.gz | awk -F" " '{ print $5 }'`
if [[ $size -gt $OTT_MIN_SIZE ]]
then
  echo "gunzip ${OTT_DUMP}.gz"
  rm -f ${OTT_DUMP}
  gunzip ${OTT_DUMP}.gz
else
  echo "ERROR: ${OTT_DUMP}.gz (from $OTT_SCHEMA schema) is not big enough at $size (less than $OTT_MIN_SIZE bytes)"
fi

size=`ls -Hltr ${OTT_DUMP} | awk -F" " '{ print $5 }'`
if [[ $size -gt $OTT_MIN_SIZE ]]
then
  # test integrity of the dump file 

  # move the current ott schema
  drop_schema;

  # load ott schema db from tar
  echo "restore ott dump"
  pg_restore -d $PGDBNAME ${OTT_DUMP}
  grantor "$OTT_SCHEMA";

  # vacuum analyze db
  echo "vacuum analyze"
  psql -p $PGPORT -d $PGDBNAME -U $PGUSER -c "vacuum analyze;"

  rm -f ${OTT_DUMP}.old
  mv ${OTT_DUMP} ${OTT_DUMP}.old
fi

date
echo "END < < < < < < "
