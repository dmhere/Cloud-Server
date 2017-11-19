#!/usr/bin/python2


import commands

print "content-type: text/html"
print

print """
<script>
function lw(mycname)
{

document.location='docker_remove.py?x=' + mycname;

}
function lw1(mycname)
{
document.location='docker_start.py?x=' + mycname;
}
function lw2(mycname)
{
document.location='docker_stop.py?x=' + mycname;
}

</script>
"""


print "<body bgcolor='#00ffff'>"
print "<table>"
print "<tr bgcolor='#ffff00'><th>DockerImage</th><th>ContainerName</th><th>Status</th><th>Stop</th><th>Start</th><th>Remove</th></tr>"

z=1
for i in commands.getoutput("sudo docker ps -a").split('\n'):
	if z == 1:
		z+=1
		pass
	else:
		j=i.split()
		#print j[-1]
		cStatus=commands.getoutput("sudo docker inspect {0} | jq '.[].State.Status'".format(j[-1]))
		print "<tr><td>" + j[1] + "</td><td>" + j[-1] + "</td><td>" + cStatus +  "</td><td> <input value='stop' type='button' onclick=lw2('"+j[-1]+"') />   </td><td>     <input value='start' type='button' onclick=lw1('"+j[-1]+"') /></td><td>  <input value='remove' type='button' onclick=lw('"+j[-1]+"')  /> </td></tr>"

print "</table>"
print "</body>"











