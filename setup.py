import os
import sys, socket


def writeHadoopConfigFile(name,xml):
    f = open("/usr/local/hadoop/etc/hadoop/" + name,"w")
    f.write(xml)
    f.close()


mf = open("manager","r")
sf = open("workers","r")
mip = mf.read().strip()
sip = sf.read().replace("-","")
mf.close()
sf.close()

os.system("cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys")

os.system("apt-get update -y && apt-get install python -y && apt-get install -y default-jdk && apt-get install -y curl && apt-get install -y maven && apt-get install -y python-pip && apt-get install -y python3-pip && curl -fsSL -o- https://bootstrap.pypa.io/pip/3.5/get-pip.py | python3.5 && hash -r && pip install --upgrade pip && pip install pyhdfs")

#clear first
os.system("rm -rf /usr/local/hadoop-2.9.2/ && unlink /usr/local/hadoop && rm -rf /data/hadoop/")
os.system("sed -i /JAVA_HOME/d /root/.bashrc && sed -i /hadoop/d /root/.bashrc && sed -i /StrictHostKeyChecking/d /etc/ssh/ssh_config")

#config env
os.system("echo 'export JAVA_HOME=/usr/lib/jvm/default-java/' >> /root/.bashrc")
os.system("echo 'export PATH=$PATH:/usr/local/hadoop/bin/:/usr/local/hadoop/sbin/' >> /root/.bashrc")
#config ssh
os.system("echo 'StrictHostKeyChecking no' >> /etc/ssh/ssh_config")
#config dir
os.system("mkdir -p /data/hadoop/node && mkdir -p /data/hadoop/data && mkdir -p /data/hadoop/name")

if not os.path.exists("hadoop-2.9.2.tar.gz"):
    print("Downloading Hadoop 2.9.2....")
    os.system("curl -o hadoop-2.9.2.tar.gz https://archive.apache.org/dist/hadoop/common/hadoop-2.9.2/hadoop-2.9.2.tar.gz")
    print("Download Hadoop 2.9.2 Successful...")

print("Install Hadoop 2.9.2 .....")
os.system("tar -xzf hadoop-2.9.2.tar.gz -C /usr/local/ && ln -s /usr/local/hadoop-2.9.2/ /usr/local/hadoop")
print("Finished Install Hadoop 2.9.2....")

print("Config Hadoop 2.9.2 ...")
os.system("sed -i '/export JAVA_HOME/s/${JAVA_HOME}/\/usr\/lib\/jvm\/default-java\//g' /usr/local/hadoop/etc/hadoop/hadoop-env.sh")

#core-site.xml
coreSiteXml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <!-- Default HDFS ip and port -->
    <property>
         <name>fs.defaultFS</name>
         <value>hdfs://%(mip)s:9000</value>
    </property>
    <!-- default RPC IP，and use 0.0.0.0 to represent all ips-->
    <property>
	<name>dfs.namenode.rpc-bind-host</name>
	<value>0.0.0.0</value>
    </property>
</configuration>""" % dict(mip=mip)
writeHadoopConfigFile("core-site.xml",coreSiteXml)
hdfsSiteXml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>


    <property>
       <name>dfs.permissions</name>
      <value>false</value>
   </property>

    <property>
        <name>dfs.namenode.http-address</name>
        <value>0.0.0.0:50070</value>
    </property>

    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>0.0.0.0:50090</value>
    </property>
    <property>
        <name>dfs.replication</name>
        <value>2</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/data/hadoop/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/data/hadoop/data</value>
    </property>
</configuration>
"""
writeHadoopConfigFile("hdfs-site.xml",hdfsSiteXml)

mapredSiteXml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
"""
writeHadoopConfigFile("mapred-site.xml",mapredSiteXml)

yarnSiteXml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>%(mip)s</value>
    </property>

    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>

    <property>
         <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
         <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
  <property>
    <name>yarn.resourcemanager.address</name>
    <value>%(mip)s:8032</value>
  </property>
  <property>
     <name>yarn.resourcemanager.scheduler.address</name>
     <value>%(mip)s:8030</value>
  </property>
  <property>
     <name>yarn.resourcemanager.resource-tracker.address</name>
     <value>%(mip)s:8031</value>
  </property>
  <property>
     <name>yarn.resourcemanager.admin.address</name>
     <value>0.0.0.0:8033</value>
   </property>
   <property>
      <name>yarn.resourcemanager.webapp.address</name>
      <value>0.0.0.0:8088</value>
   </property>
</configuration>
""" % dict(mip=mip)
writeHadoopConfigFile("yarn-site.xml",yarnSiteXml)

manager = mip
writeHadoopConfigFile("manager",manager)
workers = sip
writeHadoopConfigFile("workers",workers)


#format hdfs
os.system("/usr/local/hadoop/bin/hdfs namenode -format")
