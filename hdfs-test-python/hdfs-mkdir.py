import pyhdfs
import os
import sys
from hdfs_config import *

if len(sys.argv) < 2:
    print "Invalid dir name"
    sys.exit()
try:
    fs = pyhdfs.HdfsClient(hosts=hdfs_host)
    fs.mkdirs(sys.argv[1])
except Exception,e:
    print e
