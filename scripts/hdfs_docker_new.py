#!/usr/bin/python2

import commands
import cgi
import os

def install(swName,ipadd,passw):
	s_sw=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no {1} 'rpm -q {2}'".format(passw,ipadd,swName))
	if s_sw[0]!=0:
		pass		
		print "{0} not installed".format(swName)
		s_yum_sw=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} 'yum list {2}'".format(passw,ipadd,swName))
		if s_yum_sw[0]!=0:
			pass			
			print "{0} required for the program to work and doesn't present in yum".format(swName)
		else:
			pass
			print "installing {0}".format(swName)
			s_i_sw=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} 'yum install {2} -y'".format(passw,ipadd,swName))
			print "{0} installed".format(swName)
	else:
		pass
		print "{0} already installed".format(swName)

def setup(hostip,hostpass,dnNo,userName,sizeInput):
	s_docker_sservice=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no {1} systemctl start docker".format(hostpass,hostip)) #(check whether this will terminate all running container or not -- no it will not but restarting will)
	if s_docker_sservice[0]==0:	
		print "docker service started"
	dnRunCmd=[]
	dnloop=0
	import objectstorage_nfs_docker
	while dnloop<dnNo:
		objectstorage_nfs_docker.object_storage(userName,sizeInput,'192.168.56.101','dm')
		dnRunCmd.append('docker run -dit --privileged=true --name {0}-dn-{1} -v /{2}drive:/data hdp_sshsc_dhc_centos:v1'.format(userName,dnloop,userName)) #change image # apply folder variable too for space
		dnloop=dnloop+1
	dnloop=0
	while dnloop<dnNo:
		status=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} {2}".format(hostpass,hostip,dnRunCmd[dnloop])) 
		print status
		if status[0]==0:
			pass			
			#print " datanode run"
		else:
			pass
			#print "datanode not run"
		d_if=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-dn-{3} ifconfig eth0 0".format(hostpass,hostip,userName,dnloop))
		#print d_if
		d_dh=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-dn-{3} dhclient -v eth0".format(hostpass,hostip,userName,dnloop))
		#print d_dh
		print "datanode executed"	
		dnloop=dnloop+1

	nnRunCmd="docker run -dit --privileged=true --name {0}-nn hdp_sshsc_dhc_centos:v1".format(userName) # apply folder variable too for space
	commands.getstatusoutput("sudo sshpass -p {0} ssh {1} {2}".format(hostpass,hostip,nnRunCmd))

	commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-nn ifconfig eth0 0".format(hostpass,hostip,userName))
	commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-nn dhclient -v eth0".format(hostpass,hostip,userName))
	# install jq first
	install('jq','192.168.56.101','dm')
	nnip=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} 'docker exec {2}-nn ifconfig eth0 | grep inet'".format(hostpass,hostip,userName))[1].split()[1]
	print nnip
	dnip=[]
	dnloop=0
	while dnloop<dnNo:
		dnip.append(commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-dn-{3} ifconfig eth0 | grep inet".format(hostpass,hostip,userName,dnloop))[1].split()[1])
		dnloop=dnloop+1
	#print dnip
	print "hdfs-site.xml setting in docker(datanodes)"
	dnHdfsString = "<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>/data</value>\n</property>\n</configuration>"
	f=open("../tmp/hdfs-site.xml","w")
	f.write(dnHdfsString)
	f.close()
	dnloop=0
	while dnloop<dnNo:
		hdfs_copy=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker cp /webcontent/final/tmp/hdfs-site.xml {2}-dn-{3}:/etc/hadoop/hdfs-site.xml".format(hostpass,hostip,userName,dnloop))
		print hdfs_copy		
		if hdfs_copy[0]==0:
			pass
			print "copied in datanode"
		else:
			pass
			print "not copied in datanode"	
		dnloop=dnloop+1
	nnHdfsString = "<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>/name</value>\n</property>\n</configuration>"
	f=open("../tmp/hdfs-site.xml","w")
	f.write(nnHdfsString)
	f.close()
	hdfs_copy=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker cp /webcontent/final/tmp/hdfs-site.xml {2}-nn:/etc/hadoop/hdfs-site.xml".format(hostpass,hostip,userName))
	if hdfs_copy[0]==0:
		pass
		#print "copied in namenode"
	else:
		pass
		#print "not copied in namenode"	
	coreString = "<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{0}:10001</value>\n</property>\n</configuration>".format(nnip)
	f=open("../tmp/core-site.xml","w")
	f.write(coreString)
	f.close()
	dnloop=0
	while dnloop<dnNo:
		core_copy=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker cp /webcontent/final/tmp/core-site.xml {2}-dn-{3}:/etc/hadoop/core-site.xml".format(hostpass,hostip,userName,dnloop))
		if core_copy[0]==0:
			pass
			#print "copied in datanode"
		else:
			pass
			#print "not copied in datanode"	
		dnloop=dnloop+1
	core_copy_nn=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker cp /webcontent/final/tmp/core-site.xml {2}-nn:/etc/hadoop/core-site.xml".format(hostpass,hostip,userName))
	if core_copy_nn[0]==0:
		pass
		#print "copied in namenode"
	else:
		pass
		#print "not copied in namenode"	

	commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-nn hadoop namenode -format".format(hostpass,hostip,userName))
	print "start namenode service"
	service_namenode=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-nn hadoop-daemon.sh start namenode".format(hostpass,hostip,userName))
	if service_namenode[0]==0:
		pass
		#print "namenode service start"
	else:
		pass
		#print "namenode service not start"
	print "start datanode service"
	dnloop=0
	while dnloop<dnNo:
		service_datanode=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-dn-{3} hadoop-daemon.sh start datanode".format(hostpass,hostip,userName,dnloop))
		if service_datanode[0]==0:
			pass
			#print "datanode service start"
		else:
			pass
			#print "datanode service not start"
		dnloop+=1
	print "Setup done"

print "content-type: text/html"
print
#print "hello"

userName=os.environ['HTTP_COOKIE'].split(";")[0].split("=")[1]
dnNo=cgi.FormContent()['dnNo'][0]
dnSize=cgi.FormContent()['dnSize'][0]

#userName='vv'
dnNo=1
print "<pre>"
setup('192.168.56.101','dm',dnNo,userName,dnSize)
print "</pre>"
#print "hello"

print """
<form enctype='multipart/fom-data' method='POST' action='hdfs_docker_services.py'>
<input type='radio' name='op' value='upload' />Upload a file: <input type='file' name='fileup' /><br />
<input type='radio' name='op' value='remove' />remove a file: (Enter file name)<input type='text' name='filerm' /> <br />
<input type='radio' name='op' value='read' />read the data of a file: (Enter file Name) <input type='text' name='fileread' /> <br />
<input type='submit'>
</form>
"""
