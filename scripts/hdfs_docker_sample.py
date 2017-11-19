#!/usr/bin/python2

import cgi

dnNo=cgi.FormContent()['dnNo'][0]
dnSize=cgi.FormContent()['dnSize'][0]
print "content-type: text/html"
print
#dnNo=cgi.FormContent()['dnNo'][0]
#dnSize=cgi.FormContent()['dnSize'][0]
print dnNo,dnSize