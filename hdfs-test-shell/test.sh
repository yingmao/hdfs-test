#!/bin/sh
export PATH=$PATH:/usr/local/hadoop/bin/
echo 'make a 1G file...'
dd if=/dev/zero  of=file1g.data bs=1M count=1024
echo "Startup Hadoop hdfs...."
#启动hdfs
/usr/local/hadoop/sbin/start-dfs.sh
echo "Finished Startup Haoop hdfs"
echo 'mkdir ...'
hdfs dfs -mkdir /testfile/
echo 'uploading 1g file'
hdfs dfs -copyFromLocal file1g.data /testfile/file1g.data
echo 'list files'
hdfs dfs -ls /testfile/
echo 'remove dir'
hdfs dfs -rm -r /testfile/
echo 'Finished!'
echo "Shutdown Hadoop hdfs..."
#停止hdfs
/usr/local/hadoop/sbin/stop-dfs.sh
echo "Finished Stop Hadoop hdfs"
