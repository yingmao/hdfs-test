#!/bin/sh
mvn clean package
cp target/hdfs-test-1.0-SNAPSHOT.jar target/lib/
echo 'make a 1G file...'
dd if=/dev/zero  of=file1g.data bs=1M count=1024
echo "Startup Hadoop hdfs...."
#启动hdfs
/usr/local/hadoop/sbin/start-dfs.sh
echo "Finished Startup Haoop hdfs"
echo 'mkdir ...'
java -classpath "target/lib/*" hdfs.test.CreateDir /testfile/
echo 'uploading 1g file'
java -classpath "target/lib/*" hdfs.test.CopyFromLocal file1g.data /testfile/file1g.data
echo 'list files'
java -classpath "target/lib/*" hdfs.test.ListFiles /testfile/
echo 'remove dir'
java -classpath "target/lib/*" hdfs.test.RemoveItem /testfile/
echo 'Finished!'
rm -rf file1g.data
rm -rf target
echo "Shutdown Hadoop hdfs..."
#停止hdfs
/usr/local/hadoop/sbin/stop-dfs.sh
echo "Finished Stop Hadoop hdfs"
