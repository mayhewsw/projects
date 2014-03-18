#!/usr/bin/python

# names
with open("names.txt", "r") as f:
    line = f.read()

names = sorted(line[1:-1].split('","'))

def getAlphScore(name):
    Aoffset = 64
    return sum([ord(c)-Aoffset for c in name])

tot = 0
for i, name in enumerate(names):
    tot += (i+1) * getAlphScore(name)

print tot



