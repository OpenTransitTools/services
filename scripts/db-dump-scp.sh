. ~/services/scripts/db-common.sh

cd $BASEDIR

# what servers to scp the db dump? (default is maps7-10)
svrs=$*
svrs=${svrs:="maps7 maps8 maps9 maps10"}


if [[ $HOSTNAME == maps6* ]]
then
    for svr in $svrs
    do 
      echo "scp ${OTT_DUMP}.gz ${svr}:${BASEDIR} > /dev/null 2>&1"
            scp ${OTT_DUMP}.gz ${svr}:${BASEDIR} > /dev/null 2>&1
    done
else
    echo "NOT DUMPING to $svrs ... this is not running on maps10"
fi
