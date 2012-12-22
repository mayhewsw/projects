import fractions

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

def prob11(lst):
    """greatest adjacent numbers in a grid"""
    # i is row, j is column
    m = 0
    for i in range(0,20):
        for j in range(0,20):
            if(j <= 16):
                prodAcross = lst[i][j] * lst[i][j+1] * lst[i][j+2] * lst[i][j+3]
            if(i <= 16 and j <= 16):
                prodDiag = lst[i][j] * lst[i+1][j+1] * lst[i+2][j+2] * lst[i+3][j+3] 
            if(i <= 16):
                prodUp = lst[i][j] * lst[i+1][j] * lst[i+2][j] * lst[i+3][j]
            m = max(prodAcross,prodDiag,prodUp,m)
    return m

[[8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8],
[49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48, 4, 56, 62, 00],
[81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30, 3, 49, 13, 36, 65],
[52, 70, 95, 23, 4, 60, 11, 42, 69, 24, 68, 56, 1, 32, 56, 71, 37, 2, 36, 91],
[22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
[24, 47, 32, 60, 99, 3, 45, 2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
[32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
[67, 26, 20, 68, 2, 62, 12, 20, 95, 63, 94, 39, 63, 8, 40, 91, 66, 49, 94, 21],
[24, 55, 58, 5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
[21, 36, 23, 9, 75, 0, 76, 44, 20, 45, 35, 14, 0, 61, 33, 97, 34, 31, 33, 95],
[78, 17, 53, 28, 22, 75, 31, 67, 15, 94, 3, 80, 4, 62, 16, 14, 9, 53, 56, 92],
[16, 39, 5, 42, 96, 35, 31, 47, 55, 58, 88, 24, 0, 17, 54, 24, 36, 29, 85, 57],
[86, 56, 0, 48, 35, 71, 89, 7, 5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
[19, 80, 81, 68, 5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77, 4, 89, 55, 40],
[4, 52, 8, 83, 97, 35, 99, 16, 7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
[88, 36, 68, 87, 57, 62, 20, 72, 3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
[4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18, 8, 46, 29, 32, 40, 62, 76, 36],
[20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74, 4, 36, 16],
[20, 73, 35, 29, 78, 31, 90, 1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57, 5, 54],
[1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52, 1, 89, 19, 67, 4]]


