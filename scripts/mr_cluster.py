#!/usr/bin/python2

import commands
import os
import cgi

print "content-type: text/html"
print

username=os.environ['HTTP_COOKIE'].split(";")[0].split("=")[1]

namenodeIp=cgi.FormContent()['namenodeIp'][0]

jobtrackerIp=cgi.FormContent()['jobtrackerIp'][0]
jobtrackerPass=cgi.FormContent()['jobtrackerPass'][0]

jobtracker="[jobtracker]" + "\n{0}\tansible_ssh_user=root\tansible_ssh_pass={1}".format(jobtrackerIp,jobtrackerPass)

fh=open("mr_hosts.txt", 'a')
fh.write(jobtracker)
fh.close()

tasktracker="\n\n[tasktracker]"

tnNo=cgi.FormContent()['tnNo'][0]

i=1

while i<=int(tnNo):
	
	tnIp=cgi.FormContent()['tnIp{0}'.format(i)][0]
	tnPass=cgi.FormContent()['tnPass{0}'.format(i)][0]
	tasktracker += "\n{0}\tansible_ssh_user=root\tansible_ssh_pass={1}".format(dnIp,dnPass)
       	i=i+1

fh=open("mr_hosts.txt", 'a')
fh.write(tasktracker)
fh.close()
	

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

mapredSite="""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>mapred.job.tracker</name>
<value>{0}:9001</value>
</property>
</configuration>
""".format(jobtrackerIp)

f=open('mapred.xml','w')
f.write(mapredSite)
f.close()

stat = commands.getstatusoutput("sudo ansible-playbook /ansible/mr_cluster.yml -i /webcontent/scripts/mr_hosts.txt --become-user=root".format(username))

if stat[0]==0:
	print "Jobtracker and Tasktrackers successfully setup"




