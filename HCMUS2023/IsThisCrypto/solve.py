v8 = [0]*7
v9 = [0]*7

v8[0] = 0xACB7842B;
v8[1] = 0x5DFEBCAF;
v8[2] = 0x33801F1C;
v8[3] = 0x4F3FB333;
v8[4] = 0xA8F98777;
v8[5] = 0xCE40F926;
v8[6] = 0xEC339422;
v9[0] = 0xD63687D2;
v9[1] = 0x58B1472F;
v9[2] = 0x475B89F9;
v9[3] = 0xE3CDCD5D;
v9[4] = 0xEB67EA7B;
v9[5] = 0x8FF26308;
v9[6] = 0xD0E9E10E;

v8 = [str(hex(x)).lstrip('0x') for x in v8]
v9 = [str(hex(x)).lstrip('0x') for x in v9]
print(''.join(v8))
print(''.join(v9))

from hashlib import sha256, md5
from Crypto.Cipher import AES

name = b'recis'
word = b'cannibalization'
key = sha256(name).digest()
iv = md5(word).digest()
ct = open('flag.txt.enc', 'rb').read()
cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
print(cipher.decrypt(ct))
