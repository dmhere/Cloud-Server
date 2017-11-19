#!/usr/bin/python2


import cgi
import commands

print "content-type:  text/html"
print

osname=cgi.FormContent()['osname'][0]
ostype=cgi.FormContent()['ostype'][0]
cpunumber=cgi.FormContent()['cpunumber'][0]
storagesize=cgi.FormContent()['storagesize'][0]
ramsize=cgi.FormContent()['ramsize'][0]


ossetup="sudo sshpass -p dm ssh -o stricthostkeychecking=no  192.168.43.227 virt-install --name  {0} --location  /os/rhel-server-7.3-x86_64-dvd.iso  --os-type   linux  --os-variant  {1} --memory  {4} --vcpus  {2} --disk  /var/lib/libvirt/images/{0}.qcow2,size={3} --graphics  vnc,listen=0.0.0.0,port=5901  --noautoconsole".format(osname,ostype,cpunumber,storagesize,ramsize)

ossetupstatus=commands.getstatusoutput(ossetup)

if ossetupstatus[0] == 0:
	print "os setup done"
else:
	print "error"
