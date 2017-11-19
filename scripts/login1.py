#!/usr/bin/python2

import cgi

print "content-type: text/html"

#print cgi.FormContent()
username=cgi.FormContent()['userName'][0]
userpass=cgi.FormContent()['userPass'][0]
'''
username='dm'
userpass='md'
'''
#print username,userpass
f=open("../data/logindetails.txt",'r')
#print "hi"
d=f.read().split("\n")
#print d
i=3
for x in range(len(d)-1):
	p=d[x].split()
	if username==p[0] and userpass==p[1]:
		print "location: ../main_form.html"	
		print "set-cookie: userName={0}".format(username)
		print "set-cookie: userPass={0}".format(userpass)
		print
		print "hello"
		i=2
		break

if i==2:
	pass
else:
	print "location: ../index.html"
	print
	print """
	<script>
	alert("wrong user name or password")
	</script>	
	"""

