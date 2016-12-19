#!/usr/bin/python
import math

# p32
# Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

# Solved: this is a brute force hack (with one simple heuristic), but it runs in less than 20 seconds.

a = 34
b = 186
p = a*b


def ispd(a,b):
    p = str(a*b)
    sa = str(a)
    sb = str(b)

    ss = map(int, list(p + sa + sb))
    return sorted(ss) == range(1,10)
    
products = set()
for a in range(1,100):
    for b in range(100,10000):
        p = a*b
        if math.floor(math.log(9990,10)+1) > 4: break
        if ispd(a,b):
            print "{0} * {1} = {2} pandigital.".format(a, b, p)
            products.add(a*b)

print products
print sum(products)
