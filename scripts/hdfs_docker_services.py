#!/usr/bin/python2

import cgi
import commands
import os

print "content-type: text/html"
print

userName=os.environ['HTTP_COOKIE'].split(';')[0].split('=')[1]
#userName='dm'
#file_name=cgi.FormContent()['file_name'][0]
print "hello"
if op=='upload':
	print "upload"
	fileToUpload=cgi.FormContent()['fileup'][0]
	print fileToUpload
	f.open("../tmp/xx","w")
	print "hi1"
	f.write(fileToUpload)
	print "hi2"
	f.close()
	print "hi3"
	commands.getstatusoutput("docker cp /webcontent/final/tmp/xx {0}-nn:/".format(userName))
	print "hi4"
	commands.getstatusoutput("docker exec hadoop fs -put /xx /")
	print "hi5"	
	#print wordToCount
elif op=='remove':
	fileToRemove=cgi.FormContent()['filerm'][0]
	#print wordToCount
elif op=='read':
	fileToRead=cgi.FormContent()['fileread'][0]
	#print wordToCount

