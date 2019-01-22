import pyhdfs
import os
import sys
from hdfs_config import *

if len(sys.argv) < 2:
    print "Invalid dir or file name"
    sys.exit()
try:
    fs = pyhdfs.HdfsClient(hosts=hdfs_host)
    fs.delete(sys.argv[1],recursive=True)
except Exception,e:
    print e
