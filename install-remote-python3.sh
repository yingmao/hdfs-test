#!/bin/sh
rm -rf /hdfs-test/ && cd / && git clone https://github.com/myidwei/hdfs-test.git && python3 /hdfs-test/setup.py
cp master /hdfs-test/
cp slaves /hdfs-test/
cd /hdfs-test/ && ./install-local-python3.sh
