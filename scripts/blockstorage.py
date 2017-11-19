#!/usr/bin/python2

import commands
import cgi
import os

def block_storage(userName,sizeInput,userIP,userPassword):
	
	ssp="ub"
	ssIP="192.168.43.80"
	'''	
	userName=os.environ['HTTP_COOKIE'].split(';')[0].split('=')[1]
	sizeInput=cgi.FormContent()['storageSize'][0]
	userIP=cgi.FormContent()['userIP'][0]
	'''
	IQN="{0}cloud".format(userName)
	#userPassword=cgi.FormContent()['userPassword'][0]
	#lvreate on user demand

	lvMountFolder=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} mkdir /cloud/b{0}".format(userName,ssp,ssIP))
	print "hi"
	lvStatus=commands.getstatusoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no -l root {3} lvcreate --size {1}G --name b{0}lv vg1 -Wy".format(userName,sizeInput,ssp,ssIP))
	print "hello"
	if lvStatus[0]==0:
		print "b{0}lv created".format(userName)
		shareStatus=commands.getstatusoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no -l root {3} echo '\n<target {0}>\n\tbacking-store /dev/vg1/b{1}lv\n</target>' | cat >> /etc/tgt/targets.conf".format(IQN,userName,ssp,ssIP))	
		if shareStatus[0]==0:
			print "Hardisk exported"
			serviceStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} systemctl restart tgtd".format(ssp,ssIP)) #you can add option to install tgtd.
			if serviceStatus[0]==0:
				print "block storage service activated"	


	#client automation ----->

	clientSoftwareStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} rpm -q iscsi-initiator-utils".format(userPassword,userIP))
	if(clientSoftwareStatus[0]==0):
		print "iscsi-initiator-utils software is installed"
	else:
		commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} yum install iscsi-initiator-utils".format(userPassword,userIP))
		print "fuse-sshfs now installed"
				
	#to find IQN number------>

	findIQNstatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {0} iscsiadm --mode discoverydb --type sendtargets --portal {2} --discover".format(userIP,userPassword,ssIP)) 
	if(findIQNstatus[0]==0):
		print "discovery packet sent"
	else:
		print findIQNstatus

	#to login----->

	loginStatus=commands.getstatusoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no -l root {1} iscsiadm --mode node --targetname {0} --portal {3}:3260 --login".format(IQN,userIP,userPassword,ssIP)) 
	if(findIQNstatus[0]==0):
		print "client is successfully logged in!"
	else:
		print loginStatus
		print "failed to login"
'''
print "content-type: text/html"
print	
block_storage()
print """
Object services Created Successfully
<form action=object_forward.py>
<input type='radio' name='x' required />To extend Size <br />
<input type='radio' name='x' required />To unmount <br />
</form>
"""
'''

