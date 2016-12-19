#!/usr/bin/python

# circular primes
from eulerproject import isPrime

# SOLUTION: brute force.

def rotations(lst):
    yield lst
    for i in range(len(lst)):
        first = lst.pop(0)
        lst.append(first)
        yield lst


def circular(n):
    """ Returns whether or not n is a circular prime """
    if not isPrime(n):
        return False
    
    digits = map(int, list(str(n)))
    
    for p in rotations(digits):
        
        intp = int("".join(map(str, p)))
        if not isPrime(intp):
            return False

    return True


num = 0
for i in range(1000000):
    if circular(i):
        print i
        num += 1

print num

