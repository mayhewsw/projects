#!/usr/bin/python

import math

def prob12():

    mem = {}
    
    mx = 0
    for i in range(1, 5000000):

        nt = numdivisors(triangle(i), mem)

        #print triangle(i), nt
        
        if nt > mx:
            mx = nt
            print mx
            
        if nt > 500:
            print "Found it! i={}, triangle(i)={}".format(i, triangle(i))
            break
        
        #if i%10000 == 0:
        #    print "iteration", i
            #print mem
        

import operator as op
def multiply(d):
    ''' d looks like: {factor: exponent, ... }
    This multiplies all exponents together '''
    return reduce(op.mul, map(lambda v: v+1, d.values()))


def combine(a, b):
    ''' This adds two dictionaries '''
    return dict( (n, a.get(n, 0)+b.get(n, 0)) for n in set(a)|set(b) )


def numdivisors(n, mem = {}):
    ''' get the number of divisors of n '''
    return multiply(divisormap(n,mem))


def divisormap(n, mem):
    ''' get a map of the prime divisors (memoized) '''
    if n in mem:
        return mem[n]
    
    s = math.sqrt(n)

    i = 2
    while n%i != 0 and i <= s:
        i += 1

    # i is a prime divisor of n
    d = {i : 1}

    if i > s:
        mem[n] = {n : 1}
        return mem[n]
    
    mem[n] = combine(d, divisormap(n/i, mem))
    return mem[n]
        

def triangle(n):
    ''' Return the n-th triangular number '''
    return (n+1)*n / 2

prob12();
