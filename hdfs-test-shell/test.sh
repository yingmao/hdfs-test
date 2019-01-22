#!/bin/sh
export PATH=$PATH:/usr/local/hadoop/bin/
echo 'make a 2G file...'
dd if=/dev/zero  of=file2g.data bs=1M count=2048
echo 'mkdir ...'
hdfs dfs -mkdir /testfile/
echo 'uploading 2g file'
hdfs dfs -copyFromLocal file2g.data /testfile/file2g.data
echo 'list files'
hdfs dfs -ls /testfile/
echo 'remove dir'
hdfs dfs -rm -r /testfile/
echo 'Finished!'
