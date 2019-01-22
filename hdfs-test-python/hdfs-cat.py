import pyhdfs
import os
import sys
from hdfs_config import *

if len(sys.argv) < 2:
    print "Invalid file name"
    sys.exit()
try:
    fs = pyhdfs.HdfsClient(hosts=hdfs_host)
    f = fs.open(sys.argv[1])
    print f.read()
    f.close()
except Exception,e:
    print e
