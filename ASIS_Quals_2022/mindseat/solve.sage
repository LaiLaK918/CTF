from output import *
from gmpy2 import iroot, is_prime, lcm
from Crypto.Util.number import *
nbit = 256
pubs = PUBKEYS
encs = ENCS
_ps = []
for n, s in pubs:
    _p2 = n%(2**24)
    _p, check = iroot(_p2, 2)
    # assert check and is_prime(_p)
    _ps.append(_p)
# print(_ps)
k = 134


def recover_primes(S, P, k, _p):
    delta, check = iroot(S**2 - 4*P, 2)
    x1 = (S + delta)//2
    x2 = (S - delta)//2
    assert x1*x2 == P and x1 + x2 == S
    return (x1 << k) + _p, (x2 << k) + _p, x1, x2

factors = []
for i in range(4):
    n, s = pubs[i]
    _p = _ps[i]
    _n = (n - (_p**2))//(2**k)
    Sum = _n % (2**k)
    while Sum % _p:
        Sum += (2**k)
    xy = (_n - Sum)//(2**k)
    Sum //= _p
    p, q, x, y = recover_primes(Sum, xy, k, _p)
    factors.append((p, q))
    assert p*q == n
    
def solve(p, s, c, k):
    t = int(p-1)
    assert t % 2**k == 0

    t = t//2**k
    a = pow(s, t, p)
    b = pow(c, t, p)
    return discrete_log(b, Mod(a, p))
res = b''
for (n, s), (p, q), c in zip(pubs, factors, encs):
    res += long_to_bytes(solve(p, s, c, k))
    
print(res.decode())