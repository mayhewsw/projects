#!/usr/bin/python

def factor(a):
    """ Factor a number. (not used) """
    fs = []
    while True:
        # get a divisor
        div = -1
        for i in range(2, int(a/2.)):
            if a%i ==0:
                div = i
                break
        if div > -1:
            fs.append(div)
            a /= div
        else:
            fs.append(a)
            break
    return fs


def simplify(an, ad):
    """ Given fraction an/dn, simplify (not used) """
    while True:
        div = False
        for i in range(2, int(an/2.)):
            if an%i ==0 and ad%i==0:
                an /= i
                ad /= i
                div = True
        if not div:
            break
    return (an, ad)

for n in range(10,100):
    for d in range(n+1, 100):
        sn = list(str(n))
        sd = list(str(d))

        dec = float(n) / d
        
        for i in [0,1]:
            for j in [0,1]:
                a = float(sn[i])
                b = float(sd[j])
                if b != 0 and a / b == dec and sn[1-i] is not "0" and sn[1-i] == sd[1-j]:
                    print sn[1-i], sd[1-j]
                    print n,"/",d, "-->", sn[i],"/",sd[j]
                

        
# num = 387296
# den = 38729600
# WEIRD!                  
