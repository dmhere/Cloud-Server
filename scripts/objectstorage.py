#!/usr/bin/python2
import commands
import cgi

def object_storage():
	#userName=cgi.FormContent()['userName'][0]
	userName='dm'
	userIP='192.168.43.80'
	userPassword='ub'
	sizeInput='1'	
	'''
	sizeInput=cgi.FormContent()['storageSize'][0]
	userIP=cgi.FormContent()['userIP'][0]
	userPassword=cgi.FormContent()['userPassword'][0]
	'''	
	cloudIP="192.168.43.63"	#clouIP and storageServerIP are always same!
	ssIP="192.168.43.63"   #ss=storage server
	ssp="dm"

	#lvreate on user demand

	lvMountFolder=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} mkdir /cloud/{0}".format(userName,ssp,ssIP))
	print lvMountFolder
	lvStatus=commands.getstatusoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no -l root {3} lvcreate --size {1}G --name {0}lv vg1 -Wy".format(userName,sizeInput,ssp,ssIP))
	print lvStatus
	if lvStatus[0]==0:
		print "{0}lv created".format(userName)
		lvformatStatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} mkfs.ext4 /dev/vg1/{0}lv".format(userName,ssp,ssIP))
		if lvformatStatus[0]==0:
			print "{0}lv formatted".format(userName)
			lvMountStatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} mount /dev/vg1/{0}lv /cloud/{0}".format(userName,ssp,ssIP))
			if lvMountStatus[0]==0:
				print "{0}lv mounted".format(userName)
				commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} chown apache /etc/fstab".format(ssp,ssIP))
				print "hello flag"
				commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} chmod 700 /etc/fstab".format(ssp,ssIP))
				print "hello flag2"				
				pMountStatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} echo	/dev/vg1/{0}lv	/cloud/{0}	vfs	defaults	1	2 | cat >> /etc/fstab".format(userName,ssp,ssIP))
				#if pMountStatus[0]==0:
				print "permanent mounting done"

				shareStatus=commands.getstatusoutput("sudo sshpass -p {2} ssh -o stricthostkeychecking=no -l root {3} echo '\n/cloud/{0} {1}(rw,no_root_squash)' | cat >> /etc/exports".format(userName,userIP,ssp,ssIP))					
				if shareStatus[0]==0:
					print "data file exported"
#adding user nd making it the owner of folder.
					useraddStatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} useradd {0}".format(userName,ssp,ssIP))
					folderAccessStatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} chown {0} /cloud/{0}".format(userName,ssp,ssIP))
					folderAccess=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} chmod 700 /cloud/{0}".format(userName,ssp,ssIP)) #not using this variable!						

					if (useraddStatus[0]==0 and folderAccessStatus[0]==0):
						print "usercreated & folder owned by the user successfully"
				
						serviceStatus=commands.getstatusoutput("sudo sshpass -p {1} ssh -o stricthostkeychecking=no -l root {2} systemctl restart sshd") 
						if (serviceStatus[0]==0):
							print "object storage service activated"


			
	#client automation ------
	#check for software? ---> 1.fuse-sshfs 
	clientSoftwareStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} rpm -q fuse-sshfs".format(userPassword,userIP))
	if(clientSoftwareStatus[0]==0):
		print "fuse-sshfs software is installed"
	else:
		commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} yum install fuse-sshfs".format(userPassword,userIP))
		print "fuse-sshfs now installed"
	#2.sshpass 
	clientSoftwareStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} rpm -q sshpass".format(userPassword,userIP))
	if(clientSoftwareStatus[0]==0):
		print "sshpass software is installed"
	else:
		commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} yum install sshpass".format(userPassword,userIP))
		print "sshpass now installed"
	#...................
	#making client folder:
	clientFolderStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} mkdir /media/{2}drive".format(userPassword,userIP,userName))

	if(clientFolderStatus[0]==0):
		print "Client folder created"
	else:
		print"Client folder not cretated"

	#mounting that folder:
		
	clientServiceStatus=commands.getstatusoutput("sudo sshpass -p {0} ssh -o stricthostkeychecking=no -l root {1} sshpass -p {0} sshfs -o stricthostkeychecking=no {3}@{2}:/cloud/{3} /media/{3}drive".format(userPassword,userIP,ssIP,userName))

	if(clientServiceStatus[0]==0):
		print "my drive created"
	else:	
		print "mydrive not created"

		

print "content-type: text/html"
print	
object_storage()
print """
Object services Created Successfully
<form action=object_forward.py>
<input type='radio' name='x' required />To extend Size <br />
<input type='radio' name='x' required />To unmount <br />
</form>
"""

