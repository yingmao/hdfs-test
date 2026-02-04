#!/bin/sh
export PATH=$PATH:/usr/local/hadoop/bin/
echo 'make a 1G file...'
dd if=/dev/zero  of=file1g.data bs=1M count=1024
echo "Startup Hadoop hdfs...."
#start hdfs
/usr/local/hadoop/sbin/start-all.sh
echo "Finished Startup Haoop hdfs"
echo 'mkdir ...'
python hdfs-mkdir.py /testfile/
echo 'uploading 1g file'
python hdfs-copy-from-local.py file1g.data /testfile/file1g.data
echo 'list files'
python hdfs-list.py /testfile/
echo 'remove dir'
python hdfs-delete.py /testfile/
echo 'Finished!'
rm -rf file1g.data
echo "Shutdown Hadoop hdfs..."
#stop hdfs
/usr/local/hadoop/sbin/stop-dfs.sh
echo "Finished Stop Hadoop hdfs"
