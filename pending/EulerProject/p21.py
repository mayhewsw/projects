#!/usr/bin/python
import math

def getPropDivisorSum(n):
    s = 0
    for i in range(1, n/2 + 1):
        if n%i == 0:
            s += i
    return s


def isAmic(a):
    b = getPropDivisorSum(a)
    aprime = getPropDivisorSum(b)
    return aprime == a and a != b

print getPropDivisorSum(8128)

tot = 0
for i in range(10001):
    if isAmic(i):
        print i
        tot += i
print tot
    
