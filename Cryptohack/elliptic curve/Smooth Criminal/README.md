```sage
p = 310717010502520989590157367261876774703
a = 2
b = 3

E = EllipticCurve(GF(p), [a,b])
G = E(179210853392303317793440285562762725654, 105268671499942631758568591033409611165)
B = E(272640099140026426377756188075937988094, 51062462309521034358726608268084433317)
A = E(280810182131414898730378982766101210916, 291506490768054478159835604632710368904)
b = G.discrete_log(A)
n = (B * b)[0]
print(n)
```

```sage
171172176587165701252669133307091694084
```

```sage
def decrypt_flag(shared_secret: int, iv: str, encrypted: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]

    iv = bytes.fromhex(iv)
    encrypted = bytes.fromhex(encrypted)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(encrypted)
    return plaintext
enc = {'iv': '07e2628b590095a5e332d397b8a59aa7', 'encrypted_flag': '8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af'}
iv = enc['iv']
encrypted_flag = enc['encrypted_flag']

print(decrypt_flag(n, iv, encrypted_flag))
```

```sage
b'crypto{n07_4ll_curv3s_4r3_s4f3_curv3s}\n\n\n\n\n\n\n\n\n\n'
```
