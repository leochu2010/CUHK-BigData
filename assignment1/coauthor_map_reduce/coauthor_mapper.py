#!/usr/bin/python

import sys

for line in sys.stdin:    
    print '%s\t%s' % (line.strip(), 1)
    