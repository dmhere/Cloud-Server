#!/usr/bin/python2

import commands
import cgi
import os

print "content-type: text/html"
print

drive="dm"

namenodeIp=cgi.FormContent()['namenodeIp'][0]
namenodePass=cgi.FormContent()['namenodePass'][0]

stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} systemctl stop firewalld".format(namenodePass,namenodeIp)) 

if stat[0] != 0:
	print "Error in stopping firewall service!"
	exit()

stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} mkdir -p /{2}/name".format(namenodePass,namenodeIp,drive))

if stat[0] != 0:
	print "Error while setting up namenode in mkdir!"
	exit()

hdfsSite="""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.name.dir</name>
<value>/{0}/name</value>
</property>

</configuration>
""".format(drive)

f=open('../uploads/hdfs_name.xml','w')
f.write(hdfsSite)
f.close()

uploadHdfs=commands.getstatusoutput("sudo sshpass -p {0} scp ../uploads/hdfs_name.xml root@{1}:/etc/hadoop/hdfs-site.xml".format(namenodePass,namenodeIp))

if uploadHdfs[0] != 0:
	print "Error while setting up namenode in hdfs!"
	exit()

coreSite="""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://{0}:10001</value>
</property>


</configuration>
""".format(namenodeIp)

f=open('../uploads/coredfs_name.xml','w')
f.write(coreSite)
f.close()

uploadCore=commands.getstatusoutput("sudo sshpass -p {0} scp ../uploads/coredfs_name.xml root@{1}:/etc/hadoop/core-site.xml".format(namenodePass,namenodeIp)) 

if uploadCore[0] != 0:
	print "Error while setting up namenode in core!"
	exit()

stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} 'echo Y | hadoop namenode -format'".format(namenodePass,namenodeIp))

if stat[0] != 0:
	print "Error while setting up namenode in format!"
	exit()

stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} hadoop-daemon.sh start namenode".format(namenodePass,namenodeIp))

if stat[0] != 0:
	
	stat = commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} hadoop-daemon.sh stop namenode".format(namenodePass,namenodeIp))

	stat =commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} hadoop-daemon.sh start namenode".format(namenodePass,namenodeIp))
	
print "Namenode at {0} is successfully setup..".format(namenodeIp)

stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} 'jps | grep NameNode'".format(namenodePass,namenodeIp))

if stat[0] != 0:
	print "Namenode is not setup on this IP <br /> Please setup namenode or give valid namenode IP<br />"
	exit()

#datanode

dnNo=cgi.FormContent()['dnNo'][0]

i=1

while i<=int(dnNo): 

	datanodeIp=cgi.FormContent()['dnIp{0}'.format(i)][0]
	datanodePass=cgi.FormContent()['dnPass{0}'.format(i)][0]
	
	stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} systemctl stop firewalld".format(datanodePass,datanodeIp))

	if stat[0] != 0:
		print "Error in stopping firewall service!"
		exit()

	chkHdp=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} hadoop version".format(datanodePass,datanodeIp))

	if chkHdp[0] != 0:
		print "Hadoop not installed..\nInstall hadoop software first!" 

	stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} mkdir -p /{2}/data".format(datanodePass,datanodeIp,drive))

	if stat[0] != 0:
		print "Error while setting up datanode creating dir!"
		exit()
	
	hdfsSite="""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.data.dir</name>
<value>/{0}/data</value>
</property>

</configuration>
	""".format(drive)

	print hdfsSite	

	f=open('../uploads/hdfs_data.xml','w')
	f.write(hdfsSite1)
	f.close()

	uploadHdfs=commands.getstatusoutput("sudo sshpass -p {0} scp ../uploads/hdfs_data.xml root@{1}:/etc/hadoop/hdfs-site.xml".format(datanodePass,datanodeIp))

	if uploadHdfs[0] != 0:
		print "Error while setting up datanode in hdfssite!"
		exit()

	coreSite="""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>fs.default.name</name>
<value>hdfs://{0}:10001</value>
</property>


</configuration>
	""".format(namenodeIp)

	f=open('../uploads/coredfs_data.xml','w')
	f.write(coreSite)
	f.close()

	uploadCore=commands.getstatusoutput("sudo sshpass -p {0} scp ../uploads/coredfs_data.xml root@{1}:/etc/hadoop/core-site.xml".format(datanodePass,datanodeIp))
	
	if uploadCore[0] != 0:
		print "Error while setting up datanode in coresite!"
		exit()

	stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} hadoop-daemon.sh start datanode".format(datanodePass,datanodeIp))

	if stat[0] != 0:
		stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} hadoop-daemon.sh stop datanode".format(datanodePass,datanodeIp))

		stat=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} hadoop-daemon.sh start datanode".format(datanodePass,datanodeIp))

	print "Datanode at {0} is successfully setup..".format(datanodeIp)

	i=i+1

