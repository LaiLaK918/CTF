from pwn import remote
import time
from sage.all import *
import random

time.time()

def gen_key(user_id, n):
    random.seed(user_id)
    return [random.randrange(1024) for i in range(n)]

len_flag = 26
keys = []
cs = []

io = remote('cry1.chall.ctf.blackpinker.com', 443, ssl=True)
for i in range(26):
    io = remote('cry1.chall.ctf.blackpinker.com', 443, ssl=True)
    # io = remote('172.26.52.24', 11111)
    user_id = int(time.time()-0.1)
    key = gen_key(user_id, len_flag)

    print(io.recvline())
    c = int(io.recvline()[27:-1])
    print(c)
    # print(io.recvline())
    print(key)
    cs.append(c)
    keys.append(key)
    time.sleep(2)

print(keys)
print(cs)
A = Matrix(keys)
b = vector(cs)
print(bytes(list(A**-1*b)))
