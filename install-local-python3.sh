#!/bin/sh
python3 /hdfs-test/setup.py
cat slaves | while read line
do
    echo "Copy data to $line"
    scp -r /hdfs-test root@$line:/
    echo "Setup $line"
    ssh root@$line -n "cd /hdfs-test/ && python3 setup.py"
done
