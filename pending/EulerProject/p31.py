#!/usr/bin/python

# Ugly but effective.

def func():
    cnt = 0
    for a in range(201):
        for b in range(0, 201-a, 2):
            for c in range(0, 201-a-b, 5):
                for d in range(0, 201-a-b-c, 10):
                    for e in range(0, 201-a-b-c-d, 20):
                        for f in range(0, 201-a-b-c-d-e, 50):
                            for g in range(0, 201-a-b-c-d-e-f, 100):
                                for h in range(0, 201-a-b-c-d-e-f-g, 200):
                                    if a + b + c + d + e + f + g + h == 200:
                                        cnt += 1
    print cnt
        

if __name__ == "__main__":
    func()
