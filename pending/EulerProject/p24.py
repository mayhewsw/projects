#!/usr/bin/python

import itertools

c = 0
for i in itertools.permutations(range(10)):
    if c == 1000000-1:
        print "".join(map(str, i))
        break
    c += 1

