#!/usr/bin/python

from decimal import *

def func():
    # This needs to be high enough. How can we figure out how high to make this??
    getcontext().prec = 5000

    mx = (0,0)
    
    for i in range(1, 1000):
        print i
        v = Decimal(1) / Decimal(i)
        s = str(v)
        done = False
        
        for start in range(len(s)-2):
            s = s[start:]
            for dbl in range(1, len(s)-1, 2):
                ss = s[:dbl+1]
                sf = ss[:len(ss)/2]
                sl = ss[len(ss)/2:]
                if sf == sl:
                    #check it continues
                    safter = s[dbl+1:dbl + (dbl + 1)/2 + 1]
                    if safter == sf and safter == sl:
                        n = (dbl+1)/2
                        if n > mx[0]:
                            mx = (n, i)
                        done = True
                        break #dbl loop
            if done:
                break # start loop
    print mx


if __name__ == "__main__":
    func()
