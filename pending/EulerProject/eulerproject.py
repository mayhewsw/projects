import fractions
import math

def prob1():
    """Add all natural numbers < 1000 that are multiples of 3 or 5"""
    sum = 0
    for i in range(1000):
        if i%3 == 0 or i%5 == 0:
            sum = sum + i

    return sum

def fib(n):
    if (n == 0 or n == 1):
        return n
    else:
        return fib(n-1) + fib(n-2)

def prob2():
    """Sum of all even-valued terms in the Fibonacci sequence < 4,000,000"""
    i = 0
    n = fib(i)
    sum = 0
    while (n < 4000000):
        if(n%2 == 0):
            sum = n + sum
        i += 1
        n = fib(i)
    return sum


def isPrime(n):
    '''check if integer n is a prime'''
    n = abs(int(n))
    if n < 2:
        return False

    if n == 2:
        return True

    if not n & 1:
        return False

    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:
            return False
    return True

def prob3(n):
    """Largest prime factor of a composite number"""
    if isPrime(n):
        return 1

    x = int(n**0.5)
    if x%2 == 0:
        x += 1       # make sure x is odd

    #probably divisible by a number less than 100
    #run a loop and divide until it is not divisible any more
    oldN = -1
    while(oldN != n):
        oldN = n
        for i in range(100,1):
            if n%i == 0:
                n = n/i
                break
    
    while(x > 0):
        #print x
        if( n%x == 0 and isPrime(x)):
            return x
        x -= 2
        
    return 1

def reverse(s):
    res = ""
    for x in s:
        res = x + res
    return res

def isPalindrome(n):
    return int(reverse(str(n))) == n

def prob4():
    """Largest palindrome made from product of two 3 digit numbers"""
    m = [0,0]
    for a in range(999,99,-1):
        for b in range(999,99,-1):
            if(isPalindrome(a*b)):  
                if(a*b > m[0] * m[1]):
                    m = a,b
                
                
    return m
        
def lcm(a, b):
    return a*b/fractions.gcd(a,b)

def prob5(start,stop):
    """smallest number divisible fy each of the numbers 1 to 20"""
    r = range(start, stop+1)

    t = 1
    for i in r:
        l = lcm(t,i)
        if l != i:
            t = l
        else:
            t = t*i
    
    return t

def prob6(n):
    """difference of sum of squares and square of sums"""
    s = n*(n+1)/2
    
    ss = 0
    for i in range(1,n+1):
        ss = i**2 + ss     
    
    return abs(ss-s**2)

def prob7(n):
    """10001st prime"""
    nth = 1
    i = 1
    while(nth <= n):
        i += 1
        if isPrime(i):
            nth += 1
        

    return i
        
def prob8(n):
    """largest product of 5 consecutive digits in the 1000 digit number"""
    s = str(n)
    m = 0
    while (s != ""):
        con = s[0:5]
        mult = 1
        for i in con:
            mult = int(i) * mult
        if mult > m:
            m = mult

        s = s[1:-1]

    return m
    
def prob9():
    """find only pythogorean triplet such that a + b + c = 1000"""
    for i in range(1,1001):
        print i
        for j in range(1,1001):
                if (i**2 + j**2 ==  (1000-i-j)**2):
                    return i, j, (1000-i-j)

def prob10():
    """calculate sum of all primes < 2 million"""
    s = 2
    for i in range(3,2000000,2):
        if isPrime(i):
            s += i
        
    return s


