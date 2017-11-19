#!/usr/bin/python2

import commands

print "content-type: text/html"
print

print """
<form action='mr_client_services.py' id='mr_client_form'>
Select file name(with address): 
<select name='file_name'>
"""
z=1
for i in commands.getstatusoutput("sudo hadoop fs -ls /")[1].split("\n"):
	if z==1:
		z=z+1
	elif i.split()[1]=='-':
		pass
	else:
		print "<option>"+i.split()[-1]+"</option>"


print """
</select> <br />
Enter operation to be performed :
<br /> <input type='radio' value='wordcount' name='op' /> WordCount <input name='wordToCount' placeholder='Enter word which to count'><br />

<br /> <input type='radio'value='wordsearch' name='op' /> WordSearch <input name='wordToSearch' placeholder='Enter word to search'><br />

<br /> <input type='radio' value='mean' name='op' /> Find Mean<br />

<br /> <input type='radio' value='median' name='op' /> Find Median<b1r />

<br /> <textarea rows='6' col='40' name="code" form='mr_client_form''/></textarea>

<br /> <input type='submit' />
</form>
"""
