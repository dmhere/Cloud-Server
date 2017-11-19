#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"


username=cgi.FormContent()['userName'][0]
userpass=cgi.FormContent()['userPass'][0]

print "content-type: text/html"
print
a=commands.getstatusoutput("sudo sshpass -p dm ssh -o stricthostkeychecking=no 192.168.43.227 useradd sumo")
b=commands.getstatusoutput("sudo echo dm | passwd  sumo --stdin")
print a,"<br />"
print b,"<br />"
print "user created"
