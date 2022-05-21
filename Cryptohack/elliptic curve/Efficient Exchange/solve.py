p = 9739
E = EllipticCurve(GF(p),[497,1768])
q_x = 4726
nB = 6534
F = Zmod(p)
q_x = F(q_x)
y_2 = F(q_x^3+497*q_x+1768)
y = pow(y_2, (p+1)//4, p)
Q_A = E(q_x, y)
print(nB*Q_A)
