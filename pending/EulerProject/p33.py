#!/usr/bin/python


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
