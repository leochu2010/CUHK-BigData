#!/usr/bin/python

import sys
currentCoAuthor = None
currentCount = 0
coAuthor = None

for line in sys.stdin:
    line = line.strip()
    coAuthor, count = line.split('\t',1)
    
    try:
        count = int(count)
    except ValueError:
        continue
    
    if currentCoAuthor == coAuthor:
        currentCount += count
    else:
        if currentCoAuthor:
            print '%s\t%s' % (currentCoAuthor, currentCount)
        currentCount = count
        currentCoAuthor = coAuthor
    
if currentCoAuthor == coAuthor:
    print '%s\t%s' % (currentCoAuthor, currentCount)   
     


