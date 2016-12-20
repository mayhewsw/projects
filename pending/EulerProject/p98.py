#!/usr/bin/python

from itertools import permutations
import math

with open("p098_words.txt") as f:
    line = f.read().replace("\"", "")

names = line.split(",")


def getanagrams(n):
    ret = []
    for name in names:
        if name == n:
            continue
        if len(name) != len(n):
            continue
        if sorted(list(n)) == sorted(list(name)):
            ret.append(name)

    return ret

def numreplace(name, dct):
    ret = ""
    for c in name:
        ret += str(dct[c])
        
    if ret[0] == "0":
        # something that is definitly not a square
        return 2
    
    return int(ret)

def issquare(n):
    sn = math.sqrt(float(n))
    return int(sn) == sn

def getsquare(a, b):
    letters = set()
    # intialize
    for c in a:
        letters.add(c)
    letters = sorted(list(letters))

    nums = range(10)
    for p in permutations(nums, len(letters)):
        dct = dict(zip(letters, p))
        aint = numreplace(a, dct)
        bint = numreplace(b, dct)
        if issquare(aint) and issquare(bint):
            print a, b
            print aint, bint
            print
        

for name in names:
    an = getanagrams(name)
    if len(an) > 0:
        getsquare(name,an[0])

# Given two words, assign letters to digits such that both resulting numbers are squares.
        
