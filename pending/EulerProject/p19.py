#!/usr/bin/python

# wow, this is just really fiddly.

def dayadd(day, num):
    """ This gives you num days after day.
    For example, day=thurs, num=2, returns sat""" 
    days = ["mon", "tues", "weds", "thurs", "fri", "sat", "sun"]
    return days[(days.index(day) + num)%7]


# these months only have 30 days
shortmth = ["sept", "apr", "jun", "nov"]

mths= ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sept", "oct", "nov", "dec"]

# I just happen to know that jan 1, 1901 was a Tuesday
firstdaynextmth = "tues"
totalsun = 0

for year in range(1901, 2001):
    print "in year ", year
    for mth in mths:
        print "first day of ", mth, " is ", firstdaynextmth
        
        if mth in shortmth:
            mthlen = 30
        elif mth == "feb":
            if year%4 == 0:
                mthlen = 29
            else:
                mthlen = 28
        else:
            mthlen = 31
            
        firstdaynextmth = dayadd(firstdaynextmth, mthlen%7)
        if firstdaynextmth is "sun":
            totalsun += 1
            
print totalsun
