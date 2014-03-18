#!/usr/bin/python

def getPropDivisorSum(n):
    s = 0
    for i in range(1, n/2 + 1):
        if n%i == 0:
            s += i
    return s

abundnums = set()
for i in range(1, 28123):
    if getPropDivisorSum(i) > i:
        abundnums.add(i)


def writeas2(n):
    for an in abundnums:
        if (n-an) in abundnums:
            return True
    return False

tot = 0
for n in range(1, 28123):
    if not writeas2(n):
        tot += n

print tot
    
        
    
