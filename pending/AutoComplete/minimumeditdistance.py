from itertools import product

def LevenshteinDistance(s, t):
    ''' Computes and returns the Levenshtein Distance (an integer)
    between strings s and t'''
    
    m = len(s)
    n = len(t)

    d = []

    for i in range(n+1):
        d.append([0] * (m+1))

    for i in range(n+1):
        d[i][0] = i # the distance of any first string to an empty second string

    for j in range(m+1):
        d[0][j] = j # the distance of any second string to an empty first string

    for j in range(1, m+1):        
        for i in range(1, n+1):
            if s[j-1] == t[i-1]:
                d[i][j] = d[i-1][j-1] # no operation required
            else:
                d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1,d[i-1][j-1] + 1)

    return d[n][m]


# What I want is a language model.
# I want to be able to have some text, like:
# "going ti" and look at ngrams to find that
# "going ti" is unlikely, but "going to" is very likely.
# Given a string "<dictionary> <non-dictionary>" I want
# to be able to


# Most basically: what is the probability of having "word1" given a context of #word2"

if __name__ == "__main__":
    l = []
    l.append("982539	Abe Lincoln	was born on	February 12 , 1809")
    l.append("982544	Abe Lincoln	was born in	1809")
    l.append("992295	Abraham Lincoln	was born on	February 12 1809")
    l.append("992316	Abraham Lincoln	was born in	1809")
    l.append("992382	Abraham Lincoln	was born on	Feb.12")
    l.append("992588	Abraham Lincoln	was born in	February of 1809")
    l.append("992616	Abraham Lincoln	was born on	12th February 1809")
    l.append("992642	Abraham Lincoln	was born in	February 12 1809")
    l.append("7299805	Lincoln	was born in	February")
    l.append("7300983	Lincoln	was born in	1809")
    l.append("7301323	Lincoln	was born on	the 12th of February")


    s = "Microsoft Windows	is a registered trademark of	the Microsoft Corporation"
    
    l2 = []
    l2.append("982543	Abe Lincoln	became President of	the United States of America")
    l2.append("992254	Abraham Lincoln	became President of	the United States")
    l2.append("992242	Abraham Lincoln	became	a United States President")
    l2.append("7301385	Lincoln	became the new President of	the United States")
    #l2.append("7300041	Lincoln	became the sixteenth president of	the United States")
    l2.append("7300790	Lincoln	became president of	the United States")

    print LevenshteinDistance(l[0], s)

    #print "L"
    #for x, y in zip(l, l[1:]):    
    #    print LevenshteinDistance(x, y)

    #print
    #print "L2"
    #for x, y in zip(l2, l2[1:]):    
    #    print LevenshteinDistance(x, y)

    sum = 0
    c = 0
    for x, y in product(l, l):
        sum += LevenshteinDistance(x, y)
        c += 1

    print sum / float(c)

    sum = 0
    c = 0
    for x, y in product(l2, l2):
        sum += LevenshteinDistance(x, y)
        c += 1

    print sum / float(c)
