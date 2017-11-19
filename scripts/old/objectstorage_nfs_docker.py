#!/usr/bin/python2
import commands
import cgi

def object_storage(userName,sizeInput,userIP,userPassword):
	'''	
	userName=os.environ['HTTP_COOKIE'].split(';')[0].split('=')[1]
	#userName=cgi.FormContent()['userName'][0]
	sizeInput=cgi.FormContent()['storageSize'][0]
	userIP=cgi.FormContent()['userIP'][0]
	userPassword=cgi.FormContent()['userPassword'][0]
	'''	
	#clouIP and storageServerIP are always same!
	ssIP="192.168.43.227"   #ss=storage server
	ssp="dm"

	#lvreate on user demand

	lvMountFolder=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} mkdir /cloud/{0}".format(userName,ssp,ssIP))
	lvStatus=commands.getstatusoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no -l root {3} lvcreate --size {1}G --name {0}lv vg1 -Wy".format(userName,sizeInput,ssp,ssIP))
	if lvStatus[0]==0:
		lvformatStatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} mkfs.ext4 /dev/vg1/{0}lv".format(userName,ssp,ssIP))
		if lvformatStatus[0]==0:
			lvMountStatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} mount /dev/vg1/{0}lv /cloud/{0}".format(userName,ssp,ssIP))
			if lvMountStatus[0]==0:
				#---permanent mounting ---->			
		#		pMountStatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} 'echo \"\n/dev/vg1/{0}lv	/cloud/{0}	vfs	defaults	1	2\" | cat >> /etc/fstab'".format(userName,ssp,ssIP))
		#		if pMountStatus[0]==0:
		#			print "permanent mounting done"
				fileownStatus=commands.getstatusoutput("sudo chown apache /etc/exports")
				shareStatus=commands.getstatusoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no -l root {3} 'echo \"/cloud/{0} {1}(rw,no_root_squash)\n\" | cat >> /etc/exports'".format(userName,userIP,ssp,ssIP))					
				if shareStatus[0]==0:
					serviceStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} systemctl restart nfs".format(ssp,ssIP)) 
					


			
	#client automation ------
	#check for software? ---> 1.nfs-utils 
	clientSoftwareStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} rpm -q nfs-utils".format(userPassword,userIP))
	if(clientSoftwareStatus[0]!=0):
		commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} yum install nfs-utils".format(userPassword,userIP))
		print "nfs-utils now installed"
	
	#...................
	#making client folder:
	clientFolderStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} mkdir /{2}drive".format(userPassword,userIP,userName))

	if(clientFolderStatus[0]==0):
		pass
	else:
		print"Client folder not cretated"
	#	print clientFolderStatus

	#mounting that folder:
		
	clientServiceStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} mount {2}:/cloud/{3} /{3}drive".format(userPassword,userIP,ssIP,userName))

	if(clientServiceStatus[0]==0):
		print "Object service activated successfully!!"
	else:	
		print "mydrive not created"
		print clientServiceStatus


