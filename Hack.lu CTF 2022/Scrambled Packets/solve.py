#!/usr/bin/env python3

LB2 = 'ABCDEFGHIJKLM'
LB3 = 'IJKLMNOPQRSTUVWXYZ'
LB1 = [LB2, LB3]
with open('file.txt', 'r') as f, open('flag.txt',  'w') as w:
    i, L2, L3 = 0, 0, 0
    for line in f.readlines():
        line = line.strip()[-1]
        if line == '4':
            w.writelines(LB1[i][L3 if i == 1 else L2])
        if(i % 2 == 0):
            L2 = (L2 + 1) % len(LB2)
        else:
            L3 = (L3 + 1) % len(LB3)
        i = (i + 1) % 2
        