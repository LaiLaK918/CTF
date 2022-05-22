from sage.all import *
import json
from pwn import remote
G_x, G_y = [0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
                    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5]
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
E = EllipticCurve(GF(p), [a, b])
G = E(G_x, G_y)
P = E(0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A)
R = P.division_points(2)
print(R[0].xy()[0])

def main():
    HOST = "socket.cryptohack.org"
    PORT = 13382
    r = remote(HOST, PORT, typ='tcp')
    r.recv()
    curve = "secp256r1"
    g = [int(R[0].xy()[0]), int(R[0].xy()[1])]
    d = 2
    js = {"private_key": d, "host":"www.bing.com", "curve": curve, "generator": g}
    payload = json.dumps(js)
    r.sendline(payload)
    print(r.recv().decode())

if __name__ == '__main__':
    main()
