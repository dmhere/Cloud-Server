#!/usr/bin/python2

import commands
import os
import cgi

print "content-type: text/html"
print

#drive=os.environ['HTTP_COOKIE'].split(";")[0].split("=")[1]

drive="server1"

stat=commands.getstatusoutput("sudo mkdir /webcontent/ansible/{0}".format(drive))

stat=commands.getstatusoutput("sudo mkdir -p /{0}/name".format(drive))

stat=commands.getstatusoutput("sudo mkdir -p /{0}/data".format(drive))

namenodeIp=cgi.FormContent()['namenodeIp'][0]
namenodePass=cgi.FormContent()['namenodePass'][0]

namenode="[namenode]" + "\n{0}\tansible_ssh_user=root\tansible_ssh_pass={1}".format(namenodeIp,namenodePass)

fh=open("hosts.txt", 'a')
fh.write(namenode)
fh.close()

datanode="\n\n[datanode]"

dnNo=cgi.FormContent()['dnNo'][0]

i=1

while i<=int(dnNo):
	
	dnIp=cgi.FormContent()['dnIp{0}'.format(i)][0]
	dnPass=cgi.FormContent()['dnPass{0}'.format(i)][0]
	datanode += "\n{0}\tansible_ssh_user=root\tansible_ssh_pass={1}".format(dnIp,dnPass)
       	i=i+1

fh=open("hosts.txt", 'a')
fh.write(datanode)
fh.close()
	

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

f=open("hdfs_name.xml",'w')
f.write(hdfsSite)
f.close()

hdfsSite_dn="""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
<name>dfs.data.dir</name>
<value>/{0}/data</value>
</property>

</configuration>
""".format(drive)

f=open('hdfs_data.xml','w')
f.write(hdfsSite_dn)
f.close()

#core-site.xml

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

f=open('coredfs_name.xml','w')
f.write(coreSite)
f.close()
	
stat = commands.getstatusoutput("sudo ansible-playbook /ansible/cluster.yml -i /webcontent/scripts/hosts.txt --become-user=root".format(drive))

i=1
if stat[0]==0:
	print "HDFS cluster successfully setup"
	print "Namenode at {0}".format(namenodeIp)
	while i<=int(dnNo):
		print "{0} Datanode at IP " + dnNo{0}.format(i)
		i=i+1




