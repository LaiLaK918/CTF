from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from factordb.factordb import FactorDB
from Crypto.Util.number import isPrime, inverse, long_to_bytes, bytes_to_long

def read(n):
    key = RSA.importKey(open(f'{n}.pem', 'r').read())
    cipher = int(open(f'{n}.ciphertext', 'r').read(), 16)
    return [key.n, key.e], cipher

def solve():
    for i in range(1, 51):
        key, ct = read(i)
        r = FactorDB(key[0])
        r.connect()
        pq = r.get_factor_list()
        if len(pq) > 1:
            print(f"i = {i}")
            phi = (pq[0]-1)*(pq[1]-1)
            d = inverse(key[1], phi)
            key_rsa = RSA.construct([key[0], key[1], d])
            cipher = PKCS1_OAEP.new(key_rsa)
            pt = cipher.decrypt(long_to_bytes(ct))
            print(pt)
        else:
            continue

if __name__ == '__main__':            
    solve()
