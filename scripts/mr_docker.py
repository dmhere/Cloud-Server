#!/usr/bin/python2

import commands
import cgi
import os

def install(swName,ipadd,passw):
	s_sw=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no {1} 'rpm -q {2}'".format(passw,ipadd,swName))
	if s_sw[0]!=0:
		pass		
		#print "{0} not installed".format(swName)
		s_yum_sw=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} 'yum list {2}'".format(passw,ipadd,swName))
		if s_yum_sw[0]!=0:
			pass			
			#print "{0} required for the program to work and doesn't present in yum".format(swName)
		else:
			pass
			#print "installing {0}".format(swName)
			s_i_sw=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} 'yum install {2} -y'".format(passw,ipadd,swName))
			#print "{0} installed".format(swName)
	else:
		pass
		#print "{0} already installed".format(swName)

def setup(hostip,hostpass,ttNo,userName,nnip):
	commands.getoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no {1} systemctl start docker".format(hostpass,hostip)) #(check whether this will terminate all rujting container or not -- no it will not but restarting will)
	print "docker service started"
	ttRunCmd=[]
	ttloop=0
	while ttloop<ttNo:
		ttRunCmd.append('docker run -dit --privileged=true --name {0}-tt-{1} hdp_sshsc_dhc_centos:v1'.format(userName,ttloop)) #change image # apply folder variable too for space
		ttloop=ttloop+1
	ttloop=0
	while ttloop<ttNo:
		status=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} {2}".format(hostpass,hostip,ttRunCmd[ttloop])) 
		print status
		if status[0]==0:
			pass			
			print " tasktracker run"
		else:
			pass
			print "tasktracker not run"	
		d_if=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-tt-{3} ifconfig eth0 0".format(hostpass,hostip,userName,ttloop))
		print d_if
		d_dh=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-tt-{3} dhclient -v eth0".format(hostpass,hostip,userName,ttloop))
		print d_dh
		print "tasktracker executed"	
		ttloop=ttloop+1

	jtRunCmd="docker run -dit --privileged=true --name {0}-jt hdp_sshsc_dhc_centos:v1".format(userName) # apply folder variable too for space
	commands.getstatusoutput("sudo sshpass -p {0} ssh {1} {2}".format(hostpass,hostip,jtRunCmd))

	commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-jt ifconfig eth0 0".format(hostpass,hostip,userName))
	commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-jt dhclient -v eth0".format(hostpass,hostip,userName))
	# install jq first
	install('jq','192.168.43.227','dm')
	jtip=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-jt ifconfig eth0 | grep inet".format(hostpass,hostip,userName))[1].split()[1]
	print jtip
	ttip=[]
	ttloop=0
	while ttloop<ttNo:
		ttip.append(commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-tt-{3} ifconfig eth0 | grep inet".format(hostpass,hostip,userName,ttloop))[1].split()[1])
		ttloop=ttloop+1
	print ttip
	#hdfs-site.xml setting in docker(tasktrackers)
	mapredString = "<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>{0}:9001</value>\n</property>\n</configuration>\n".format(jtip)
	print "hi4"	
	f=open("../tmp/mapred-site.xml","w")
	print "hi1"
	f.write(mapredString)
	print "hi2"
	f.close()
	print "hi3"
	ttloop=0
	print "hi"
	while ttloop<ttNo:
		mapred_copy=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker cp /webcontent/final/tmp/mapred-site.xml {2}-tt-{3}:/etc/hadoop/mapred-site.xml".format(hostpass,hostip,userName,ttloop))
		print mapred_copy		
		if mapred_copy[0]==0:
			pass
			print "copied in tasktracker"
		else:
			pass
			print "not copied in tasktracker"	
		ttloop=ttloop+1
	mapred_copy=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker cp /webcontent/final/tmp/mapred-site.xml {2}-jt:/etc/hadoop/mapred-site.xml".format(hostpass,hostip,userName))
	if mapred_copy[0]==0:
		pass
		print "copied in jobtracker"
	else:
		pass
		print "not copied in jobtracker"	
	coreString = "<?xml version='1.0'?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{0}:10001</value>\n</property>\n</configuration>\n".format(nnip)
	f=open("../tmp/core-site.xml","w")
	f.write(coreString)
	f.close()
	ttloop=0
	core_copy_jt=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker cp /webcontent/final/tmp/core-site.xml {2}-jt:/etc/hadoop/core-site.xml".format(hostpass,hostip,userName))
	if core_copy_jt[0]==0:
		pass
		print "copied in jobtracker"
	else:
		pass
		print "not copied in jobtracker"	
	
	#start jobtracker service
	service_jobtracker=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-jt hadoop-daemon.sh start jobtracker".format(hostpass,hostip,userName))
	print service_jobtracker	
	if service_jobtracker[0]==0:
		pass
		#print "jobtracker service start"
	else:
		pass
		#print "jobtracker service not start"
	#start tasktracker service
	ttloop=0
	while ttloop<ttNo:
		service_tasktracker=commands.getstatusoutput("sudo sshpass -p {0} ssh {1} docker exec {2}-tt-{3} hadoop-daemon.sh start tasktracker".format(hostpass,hostip,userName,ttloop))
		if service_tasktracker[0]==0:
			pass
			#print "tasktracker service start"
		else:
			pass
			#print "tasktracker service not start"
		ttloop+=1
	print "Setup done"


print "content-type: text/html"
print
print "hello"

#userName=os.environ['HTTP_COOKIE'].split(";")[0].split("=")[1]
#ttNo=cgi.FormContent()['ttno'][0]
#nnip=cgi.FormContent()['nnip'][0]
ttNo=1
userName='oo'
nnip='192.168.43.106'
setup('192.168.43.227','dm',ttNo,userName,nnip)
#print "hello"
print """
<form action='hdfs_docker_services.py'>
Upload a file: <input type='file' /><br />
remove a file: (Enter file name)<input type='text' />
read the data of a file: (Enter file Name) <input type='text' />
</form>
"""
