from ast import literal_eval

lines = open("./output.txt","r").readlines()
messages = literal_eval(lines[0].strip())
enc = literal_eval(lines[1].strip())

M1 = matrix.identity(ZZ,47)
B1 = matrix(ZZ,47,1) 
for i,message in enumerate(messages):
    B1[i,0] = message

M = block_matrix(ZZ,[B1,M1],ncols = 2)
L = M.LLL()

def coompute_kn(coff):
    # \sum mi*ki = coff[0]
    if coff[0]>0:
        res_right = 1
        res_left = pow(0x10001, coff[0])
    else:
        res_right = pow(0x10001, -coff[0])
        res_left = 1
    for i ,cof in enumerate(coff[1:]):
        if cof > 0:
            res_right = res_right * enc[i]**cof
        else:
            res_left = res_left * enc[i]**(-cof)
    return res_left - res_right

n0 = coompute_kn(L[0])
for i in range(1,47):
    kn = coompute_kn(L[i])
    n0 = gcd(kn,n0)
    print("[+] nbits ",n0.nbits())
    if n0.nbits()<=1024:
        print(n0)
        break
print(n0)
# filter small factors
n0 = factor(n0,limit=2^20)
n_ = n0[-1][0]
print(f"[+] find n : {n_}")
print(f"[+] n bits : {n_.nbits()}")
from Crypto.Util.number import *
encm = enc[-1]

p = 12980311456459934558628309999285260982188754011593109633858685687007370476504059552729490523256867881534711749584157463076269599380216374688443704196597025947
q = 10104420349837363561278745998119091841853342383118385156657416134976061697027571349895988817770681767227605656666215380267313369652920490697343475330713803
assert p*q==n_
GN = GF(p)
flag = discrete_log(GN(encm),GN(0x10001))
print(long_to_bytes(int(flag)))
