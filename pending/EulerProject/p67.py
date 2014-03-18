#!/usr/bin/python

with open("triangle.txt", "r") as f:
    lines = f.readlines()

rows = []
for line in lines:
    rows.append(map(int, line.split()))

for i,row in enumerate(rows):
    if i == 0: continue
    for j,num in enumerate(row):
        if j == 0:
            plist = [j]
        elif j == len(rows[i-1]):
            plist = [j-1]
        else:
            plist = [j-1, j]
        
        pvalues = map(lambda n: rows[i-1][n], plist)
        row[j] = num + max(pvalues)

print max(rows[-1])
