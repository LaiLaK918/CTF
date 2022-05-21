```py
P.<bit, pad, x, coeff, paded_x> = PolynomialRing(ZZ)
c1 = x*(x+coeff)
paded_x = bit*x+pad
c2 = paded_x*(paded_x+coeff)
tmp1 = bit^2 * c1
tmp2 = c2 - pad*(pad+coeff)
tmp3 = bit^2 * coeff - 2*bit*pad - bit*coeff
print(f"c1: {c1}")
print(f"c2: {c2}")
print(f"tmp1: {tmp1}")
print(f"tmp2: {tmp2}")
print((tmp1-tmp2)/tmp3)
```

```py
c1: x^2 + x*coeff
c2: bit^2*x^2 + 2*bit*pad*x + bit*x*coeff + pad^2 + pad*coeff
tmp1: bit^2*x^2 + bit^2*x*coeff
tmp2: bit^2*x^2 + 2*bit*pad*x + bit*x*coeff
x
```
