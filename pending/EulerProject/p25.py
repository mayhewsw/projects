#!/usr/bin/python

d= {}

def fib_memo(n):
    ''' this returns the nth fibonacci number '''
    if n < 1:
        return "ERRORROROROROR"
    if n ==1: return 1
    if n == 2: return 1
    
    if n in d:
        return d[n]

    fibn = fib_memo(n-1) + fib_memo(n-2)
    d[n] = fibn
    return fibn

def func():
    pass

if __name__ == "__main__":
    for i in range(1, 100000):
        s = str(fib_memo(i))
        if len(s) >= 1000:
            print s
            print i
            break
            
