import pyhdfs
import os
import sys
from hdfs_config import *

if len(sys.argv) < 3:
    print "Invalid source name or target name"
    sys.exit()
try:
    fs = pyhdfs.HdfsClient(hosts=hdfs_host)
    fs.copy_from_local(sys.argv[1],sys.argv[2])
except Exception,e:
    print e
