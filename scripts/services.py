#!/usr/bin/python2

import commands
import cgi

print "content-type : text/html"
print

def display(path):
	commands.getstatusoutput("sudo sshpass -p ruhi456 ssh -o stricthostkeychecking=no -l root 192.168.43.25 hadoop fs -ls {0}".format(path))

def showReport():
	commands.getstatusoutput("sudo sshpass -p ruhi456 ssh -o stricthostkeychecking=no -l root 192.168.43.25 hadoop dfsadmin -report".format(path))

def createDir(path):
	commands.getstatusoutput("sudo sshpass -p ruhi456 ssh -o stricthostkeychecking=no -l root 192.168.43.25 hadoop fs -mkdir {0}".format(path))

def putFile(bytes,number):
	commands.getstatusoutput("sudo sshpass -p ruhi456 ssh -o stricthostkeychecking=no -l root 192.168.43.25 hadoop fs -Ddfs.block.size={0} -Ddfs.replication={1} -put {2} /".format(bytes,number,path))	
	
def remove(path):
	commands.getstatusoutput("sudo sshpass -p ruhi456 ssh -o stricthostkeychecking=no -l root 192.168.43.25 hadoop fs -rm [-skipTrash] {0}".format(path))	
	
def show(src):
	commands.getstatusoutput("sudo sshpass -p ruhi456 ssh -o stricthostkeychecking=no -l root 192.168.43.25 hadoop fs -cat {0}".format(src))

request=cgi.FormContent()['request'][0]

if request=="display":
	print "Enter absolute path : "	
	print "<input type=text name='path' value='/' />"
	display(path)		
elif request=="showReport":
	showReport()
elif request=="createDir":
	print "Enter absolute path : "
	print "<input type=text name='path' />"
	createDir(path)		
elif request=="putFile":
	print "Enter file to upload: "
	print "<input type='text' name='path' value='/' />"
	print "<br />"
	print "Enter number of replications you want: "
	print "<input type='text' name='rep' value='3' />"
	print "<br />"
	print "Enter block size you want in bytes: "
	print "<input type='text' name='block' value='67108864' />"
	print "<br />"
	putFile(block,rep)
elif request=="remove":
	print "Enter file to remove: "
	print "<input type='text' name='path' />"
	remove(path)
else:
	print "Enter file which u want to see: "
	print "<input type='text' name='path' />"
	show(path)









































 


















































