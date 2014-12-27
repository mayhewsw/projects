#!/usr/bin/python

from eulerproject import isPrime, lcd
import math

# this is slow, but I don't know of a faster way to do it.
# Also, I cheated - b is never negative. 

def func():
    mx = (0, 0,0)
    
    for a in range(-1000, 1000):
        print "a", a
        for b in range(1, 1000, 2):
            if not isPrime(b):
                continue

            if lcd(abs(a),abs(b)) < mx[0]:
                continue
            
            f = lambda x: x**2 + a*x + b
            for n in range(100000):
                if not isPrime(f(n)):
                    break
            if n > mx[0]:
                print "new max:", n
                mx = (n, a, b)
    print "mx:", mx
    print mx[1] * mx[2]


if __name__ == "__main__":
    func()
