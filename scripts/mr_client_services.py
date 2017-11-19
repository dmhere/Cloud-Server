#!/usr/bin/python2

import cgi
import commands
import os

print "content-type: text/html"
print

#userName=os.environ['HTTP_COOKIE'].split(';')[0].split('=')[1]
userName='dm'
file_name=cgi.FormContent()['file_name'][0]
op=cgi.FormContent()['op'][0]
if op=='wordcount':
	wordToCount=cgi.FormContent()['wordToCount'][0]
	#print wordToCount
	commands.getstatusoutput("sudo hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -input /{0} -mapper ./search.py -file search.py -reducer ./wordcount.py -file wordcount.py 'wc -l' -output /{1}/wordcount/{2}".format(file_name,userName,wordToCount))
	output=commands.getstatusoutput("sudo hadoop fs -cat /{0}/wordcount/{1}/part*".format(userName,wordToCount))
	print output[1]

elif op=='wordsearch':
	wordToSearch=cgi.FormContent()['wordToSearch'][0]
        print wordToSearch
        commands.getstatusoutput("sudo hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -input /{0} -mapper cat -reducer 'wc -l' -output /{1}/wordsearch/{2}".format(file_name,userName,wordToSearch))
        output=commands.getstatusoutput("sudo hadoop fs -cat /{0}/wordsearch/{1}/part*".format(userName,wordToSearch))
        print output[1]
'''
elif op=='mean':
	print "mean"

elif op=='median':
	print "median"
'''
