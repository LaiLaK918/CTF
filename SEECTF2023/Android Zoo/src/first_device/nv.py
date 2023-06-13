import struct
import binascii
import scrypt
from tqdm import tqdm

N = 16384
r = 8
p = 1
f = open("gatekeeper.pattern.key", "rb")
blob = f.read() 
s = struct.Struct('<'+'17s 8s 32s')
(meta, salt, signature) = s.unpack_from(blob)
import itertools

digits = '0123456789'
word_list = [''.join(p) for p in itertools.product(digits, repeat=5)]

for data in tqdm(word_list[::-1]):    
    password=data.strip()       
    to_hash = meta    
    to_hash += password.encode()
    hash = scrypt.hash(to_hash, salt, N, r, p)  
    if hash[0:32] == signature:  
        print(password)
        exit()