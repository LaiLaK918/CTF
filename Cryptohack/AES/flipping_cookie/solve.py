import urllib.request as rq, json
from django.shortcuts import redirect
from pwn import xor
url = "http://aes.cryptohack.org/flipping_cookie/get_cookie/"
reponse = rq.urlopen(url)
cookie = json.loads(reponse.read())

def bitFlip(pos: int, bit: int, iv: bytes):
    raw = list(iv)
    raw[pos] ^= bit
    return bytes(raw)

ct = cookie['cookie'][32:]
iv = cookie['cookie'][:32]
ct = bytes.fromhex(ct)
iv = bytes.fromhex(iv)
flip = xor(b'False', b'True;')
for i in range(6, 11):
    iv = bitFlip(i, flip[i-6], iv)
    
send_url = f"http://aes.cryptohack.org/flipping_cookie/check_admin/{ct.hex()}/{iv.hex()}"
print(send_url)
