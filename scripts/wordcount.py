#!/usr/bin/python2

import sys

def count():
	j=1
	for i in sys.stdin:
		j=j+1
	print j

count()
