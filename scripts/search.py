#!/usr/bin/python2

import sys

def search(keyword):
	for i in sys.stdin:
		if re.search(keyword,i):
			print i
		else:
			pass
