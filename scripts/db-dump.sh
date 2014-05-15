. ~/services/scripts/db-common.sh


echo "START > > > > > "
date

cd $BASEDIR

# dump trimet postgres database to tar.gz, include only the following schemas;
echo "pg_dump -n $OTT_SCHEMA $PGDBNAME -F t > $OTT_DUMP"
pg_dump -n $OTT_SCHEMA $PGDBNAME -F t > $OTT_DUMP

# check to see the size of the dump
size=`ls -ltr $OTT_DUMP | awk -F" " '{ print $5 }'`
if [[ $size -gt $OTT_MIN_SIZE ]]
then
  echo "gzip $OTT_DUMP"
  rm -f ${OTT_DUMP}.gz
  gzip $OTT_DUMP
  ./bin/db-dump-scp.sh $*
else
  echo "ERROR: ${OTT_DUMP}.gz (from $OTT_SCHEMA schema) is not big enough at $size (less than $OTT_MIN_SIZE bytes)"
fi

date
echo "END < < < < < "
