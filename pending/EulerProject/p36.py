#!/usr/bin/python
import math

def to2(n):
    powers = []

    while True:
        largest = math.floor(math.log(n, 2))
    
        powers.append(int(largest))
        n -= math.pow(2, largest)

        if n == 0:
            break
                
    zeros = ["0"]*(int(powers[0])+1)
    for p in powers:
        zeros[p] = "1"

    return "".join(zeros)

def isPalindrome(n):
    n = str(n)
    return n == n[::-1]

s = 0

for i in range(1, 1000001):
    bin = to2(i)

    if isPalindrome(i) and isPalindrome(bin):
        s += i

print s
