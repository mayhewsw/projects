#!/usr/bin/python
from eulerproject import isPrime


def isRightTruncatable(n):
    
    while True:
        if not isPrime(n):
            return False
        
        n = str(n)[:-1]

        if len(n) == 0:
            break
        
        n = int(n)
        
    return True

def isLeftTruncatable(n):
    
    while True:
        if not isPrime(n):
            return False
        
        n = str(n)[1:]

        if len(n) == 0:
            break
        
        n = int(n)
        
    return True



i = 10
s = 0
num = 0
while True:
    if isLeftTruncatable(i) and isRightTruncatable(i):
        print i
        s += i
        num += 1

    if num == 11:
        break
    
    i += 1
    
print s    
        
