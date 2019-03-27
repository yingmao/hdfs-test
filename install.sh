#!/bin/sh
python3 /hdfs-test/setup.py
cat works | while read line
do
    if [ "$line" = "-" ]; then
        echo "Skip $line"
    else
        ssh root@$line -n "rm -rf /hdfs-test/ && mkdir /hdfs-test/"
        echo "Copy data to $line"
        scp  /hdfs-test/setup.py root@$line:/hdfs-test/ && scp /hdfs-test/manager root@$line:/hdfs-test/ && scp /hdfs-test/slaves root@$line:/hdfs-test/
        echo "Setup $line"
        ssh root@$line -n "cd /hdfs-test/ && python3 setup.py"
        echo "Finished config node $line"
        echo "########################################################"
    fi
done
