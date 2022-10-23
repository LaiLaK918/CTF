from Crypto.Util.number import *

flag = []
P = 231609284865232306744388160907453774453
A = 213929627434382339098735177055751649916
B = 19199104003461693263250446715340616788
C = 81305572597778258494448971196865605263
D = 204055349607012377951682156574173649079
E = 2268211308285612387872477045295901103

def find_flag_from_roots(f, ring):
    g = f.univariate_polynomial()
    roots = g.roots(ring=ring)
    for root in roots:
        try: 
            print(long_to_bytes(int(root[0])).decode())
            flag.append(int(root[0]))
            break
        except:
            pass
        
R.<x, y, z, w> = ZZ[]
a = x^1+y^3+z^3+w^7-A
b = y^1+z^3+w^3+x^7-B
c = z^1+w^3+x^3+y^7-C
d = w^1+x^3+y^3+z^7-D
e = x+y+z+w-E

x1 = a.resultant(e, x) # reduce x, contains y, z, w
x2 = b.resultant(e, x) # reduce x
x3 = x1.resultant(x2, y) # reduce y, contains z, w
x4 = c.resultant(e, x) # reduce x
x5 = d.resultant(e, x) # reduce x
x6 = x4.resultant(x5, y) # reduce y
f = x3.resultant(x6, z) # reduce z, contains only w

# find w
find_flag_from_roots(f, Zmod(P))
# find z
find_flag_from_roots(x3.subs({w:flag[-1]}), Zmod(P))
# find y
find_flag_from_roots(x1.subs({z:flag[-1], w:flag[-2]}), Zmod(P))
# find x
find_flag_from_roots(a.subs({y:flag[-1], z:flag[-2], w:flag[-3]}), Zmod(P))
print(b''.join(long_to_bytes(x) for x in flag[::-1]).decode())
