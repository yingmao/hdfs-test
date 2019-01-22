import pyhdfs
import os
import sys
from hdfs_config import *

if len(sys.argv) < 2:
    print "Invalid dir name"
    sys.exit()
try:
    fs = pyhdfs.HdfsClient(hosts=hdfs_host)
    list = fs.list_status(sys.argv[1])
    for item in list:
        print "Type:" + item.type + ", Name:" + item.pathSuffix
except Exception,e:
    print e
