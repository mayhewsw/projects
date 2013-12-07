#!/usr/bin/python

# This is just annoying.

nums = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def numletters(n):
    ''' Count the number of letters in the textual expansion of n.
    For example, numletters(342) == 23
    because len("three hundred and forty two") == 23
    '''
    
    nlst = map(int, list(str(n)))

    if len(nlst) == 1:
        return [nums[n]]
    
    elif len(nlst) == 2:
        if nlst[0] == 1:
            return [teens[nlst[1]]]
        
        s = [tens[nlst[0]]] + numletters(nlst[1])
        return s
    
    elif len(nlst) == 3:
        s = [nums[nlst[0]], "hundred"]

        lasttwo = 10*nlst[1] + nlst[2]

        if lasttwo != 0:
            s += ["and"]
            s += numletters(lasttwo)

        return s
    
    elif len(nlst) == 4:
        return ["one", "thousand"]
    
    return ["error"]

total = 0
# 1 to 1000 inclusive
for i in range(1, 1001):
    lst = numletters(i)
    print lst
    total += sum(map(len, lst))

print total
