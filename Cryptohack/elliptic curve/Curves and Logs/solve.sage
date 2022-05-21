from hashlib import sha1
p = 9739
E = EllipticCurve(GF(9739),[497,1768])
Q_A = E(815, 3190)
nB = 1829
S = nB*Q_A
print(sha1(str(S[0]).encode()).hexdigest())
