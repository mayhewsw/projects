#!/usr/bin/python

def diagsumspiral(n):
    """
    Given a clockwise right spiral with sides of length n
    and beginning at 1 (in the center) this returns the
    sum of the diagonals of the spiral
    """
    if n == 1:
        return 1

    #np = n-1
    #vals = n**2 + n**2-np + n**2 - 2*np + n**2 - 3*np
    vals = 4*n**2 - 6*(n-1)
    return vals + diagsumspiral(n-2)
    

if __name__ == "__main__":
    print diagsumspiral(1001)
