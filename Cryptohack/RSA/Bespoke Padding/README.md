Been cooking up my own padding scheme, now my encrypted flag is different everytime!

Connect at nc socket.cryptohack.org 13386

[13386.py](https://cryptohack.org/static/challenges/13386_3d6974846ab20b12c216ff403ec9c99b.py)


# Exploit

Have n = p*q, m_pad = a*m+b; a,b are random

Enc1: (a1*m+b1)^e = c1

Enc2: (a2*m+b2)^e = c2

This looks very vunerable to the Franklin-Reiter related message attack, an attack on rsa where we have two messages of the form:

m2 = f(m1)

f(x) = ax+b

```py
def compositeModulusGCD(a, b):
    if(b == 0):
            return a.monic()
    else:
            return compositeModulusGCD(b, a % b)

def FranklinReiter(n, e, c1, c2, a1, a2, b1, b2):
    P.<x> = PolynomialRing(Zmod(n))
    f = (a1*x+b1)^e - c1
    g = (a2*x+b2)^e - c2
    m =  Integer(n-(compositeModulusGCD(f,g)).coefficients()[0])
    return m
    
```
