#!/usr/bin/python2

import commands
import cgi
import os

userName=os.environ['HTTP_COOKIE'].split(';')[0].split('=')[1]
#userName=cgi.FormContent()['userName'][0]
sizeInput=cgi.FormContent()['storageSize'][0]
userIP=cgi.FormContent()['userIP'][0]
userPassword=cgi.FormContent()['userPassword'][0]
task=cgi.FormContent()['type'][0]

print "content-type: text/html"
print

if task=='object':
	#print "object"	
	import objectstorage_nfs_docker
	objectstorage_nfs_docker.object_storage(userName,sizeInput,userIP,userPassword)
	print """
	<form action='service_stass.py'>
	<input type='radio' name='st' value='lvextend'/ > extend the size<br />
	<input type='radio' name='st' value='lvextend'/ > remove the drive<br />
	<input type='submit /'>
	"""
	
	
elif task == 'block':
	print "block"
	print "Successfully done"
	'''
	import blockstorage
	blockstorage.block_storage(userName,sizeInput,userIP,userPassword)
	print "block1"
	'''
print "{0} storage successfully created you can use the service".format(task)

