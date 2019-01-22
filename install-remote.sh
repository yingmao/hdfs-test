#!/bin/sh
rm -rf /hdfs-test/ && cd / && git clone https://github.com/yingmao/hdfs-test.git && python /hdfs-test/setup.py
cp master /hdfs-test/
cp slaves /hdfs-test/
cd /hdfs-test/ && ./install-local.sh
