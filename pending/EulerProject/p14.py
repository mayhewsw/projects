#!/usr/bin/python

# Collatz
# again, we memoize...



def collatz(n, mem):
    ''' get the collatz sequence for n '''
    
    if n in mem:
        return mem[n]

    # base case
    if n == 1:
        # no need for memoization here
        return [1]

    l = [n]
    
    if (n%2 == 0):
        l.extend(collatz(n/2, mem))
    else:
        l.extend(collatz(3*n + 1, mem))

    mem[n] = l
    return l

maxlen = 0
maxn = 0

mem = {}

for i in range(1, 1000000):
    l = collatz(i, mem)

    if(i%100000 == 0):
        print "iteration " + str(i)
    
    if len(l) > maxlen:
        maxlen = len(l)
        maxn = i

print "number is {} with collatz sequence length of: {}".format(maxn, maxlen)
    
