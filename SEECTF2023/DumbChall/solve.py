from pwn import *
from random import getrandbits

conn = remote('win.the.seetf.sg', 3002)

line = conn.recvline()
print(line)
p = int(line[4:])

line = conn.recvline()
print(line)
g = int(line[4:])

line = conn.recvline()
print(line)
y = int(line[4:])

print(conn.recvline())
print(conn.recvline())

def first_verify(g, p, y, C, w, r) -> bool:
    assert w
    return ((y * C) % p) == pow(g, w, p)


def second_verify(g, p, y, C, w, r) -> bool:
    assert r
    return pow(g, r, p) == C

seen_c = set()
for round in range(30):
    opt = conn.recv()
    print(opt)
    if b'w' in opt:
        while True:
            w = getrandbits(128)
            C = pow(g, w, p) * pow(y, -1, p)
            if not C in seen_c:
                seen_c.add(C)
                break
        conn.sendline(str(w).encode())
        conn.sendline(str(C).encode())
    elif b'r' in opt:
        while True:
            r = getrandbits(128)
            C = pow(g, r, p)
            if not C in seen_c:
                seen_c.add(C)
                break
        conn.sendline(str(r).encode())
        conn.sendline(str(C).encode())
    print(conn.recvline())

conn.interactive()
