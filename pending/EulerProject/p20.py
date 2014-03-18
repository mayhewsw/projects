#!/usr/bin/python

# That was easy...
# How to do it if you can't calculate fact(100)?
# Not sure there is any mathematical theory for that.

def fact(n):
    if n == 1:
        return 1
    return n * fact(n-1)

st = str(fact(100))

s = 0
for c in st:
    s += int(c)

print s
