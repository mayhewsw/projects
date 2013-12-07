#!/usr/bin/python
import math

for i in range(20):
    print "2^{} = ".format(i), math.pow(2, i)

# the last digit is 6.

def digitsum(n):
    print n
    ret = 0
    s = str(n)

    for c in s:
        ret += int(c)
    return ret
        
    
print digitsum(long(math.pow(2, 1000)))

