#!/usr/bin/python

# The upper limit in this problem was a shot in the dark.
# I have no proof that it is correct, but it worked!

def func():
    ret = []
    for i in range(10, 1000000):
        if ndigpower(i, 5) == i:
            ret.append(i)
            print i
    print sum(ret)

def ndigpower(i, n):
    s = str(i)
    l = list(s)
    return sum(map(lambda v: int(v)**n, l))

if __name__ == "__main__":
    func()
