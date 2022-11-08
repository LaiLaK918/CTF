from ast import literal_eval
lines = open("./output.txt","r").readlines()
fs = []
ns = []
para_s = []

def fun(n,a,b,y):
    Pn.<x> = PolynomialRing(Zmod(n))
    k = 4*(x^3+a*x+b)
    c = (3*x^2+a)^2
    f = k^3*y^2 - (c-2*x*k)^3 - a*(k^2*c-2*x*k^3) - b*k^3
    return f

for line in lines:
    n,a,b,y = [ZZ(i) for i in line.strip().split(" ")]
    f = fun(n,a,b,y).monic().change_ring(ZZ)
    fs.append(f)
    ns.append(n)
    para_s.append([n, a, b, y])
    
F = crt(fs,ns)
M = prod(ns)
FF = F.change_ring(Zmod(M))
roots = FF.small_roots(X = 2**400,epsilon = 1/40,beta = 4/7)
# m = FF.small_roots(X=2**256,beta=1.0)
print(roots)

from Crypto.Util.number import *
m = 15425251357776807541227287240467548867067510789583043568768907891381811730130189461693802496389917454461
print(m.nbits())
print(long_to_bytes(int(m)))
