# HCMUS CTF 2023

## Cryptography
### 1. Bootleg AES
This challenge includes three files: enc.sh, log.txt, and ciphertext.txt.

```bash
#!/bin/bash

echo "$(cat pad.bin)$FLAG" > flag.bin
ls -alF ./pad.bin
x=$(openssl rand -hex 32)
echo $x
openssl enc -aes-256-cbc -K $x -iv $(openssl rand -hex 16) -in flag.bin -out ciphertext.bin
```

From log.txt, it can be seen that the file pad.bin has a size of 256 bytes, and the key has a length of 256 bits. Due to the encryption process using CBC mode, the IV of the following block will be the ciphertext of the previous block. Therefore, the IV for decrypting the flag will be the last 16 bytes of the first 256 bytes in the ciphertext. With the key and IV, decrypting the flag will be completed.

```py
from Crypto.Cipher import AES

with open('ciphertext.bin', 'rb') as f:
    ct = f.read()

ct = ct
iv = ct[256-16:256]
ct_ = ct[256:]
key = bytes.fromhex('c9a391c6f65bbb38582044fd78143fe72310e96bf67401039b3b6478455a1622')
cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
print(cipher.decrypt(ct_))
```

Flag: ```HCMUS-CTF{it5-c4ll3d_pr1v4t3_k3y_crypt09raphy_f0r_4_r4350n}```

### 2. Sneak peek

Source:
```py
from Crypto.Util.number import getPrime, bytes_to_long as b2l

FLAG = b2l(b'HMCSU-CFT{SO YOU THINK THIS FLAG IS REAL\xff}')

p = getPrime(512)
q = getPrime(512)


n = p * q
peek = p >> 240

print(n)
print(peek)
print(pow(FLAG, 65537, n))
"""
137695652953436635868173236797773337408441001182675256086214756367750388214098882698624844625677992374523583895607386174643756159168603070583418054134776836804709359451133350283742854338177917816199855370966725059377660312824879861277400624102267119229693994595857701696025366109135127015217981691938713787569
6745414226866166172286907691060333580739794735754141517928503510445368134531623057
60939585660386801273264345336943282595466297131309357817378708003135300231065734017829038358019271553508356563122851120615655640023951268162873980957560729424913748657116293860815453225453706274388027182906741605930908510329721874004000783548599414462355143868922204060850666210978837231187722295496753756990
"""
```

This challenge is related to the RSA encryption system, in which prime p is missing the last 240 bits. This is a classic form of the Coppersmith attack, and there is no need to discuss it further.

Solve:

```py
n = 137695652953436635868173236797773337408441001182675256086214756367750388214098882698624844625677992374523583895607386174643756159168603070583418054134776836804709359451133350283742854338177917816199855370966725059377660312824879861277400624102267119229693994595857701696025366109135127015217981691938713787569
peek = 6745414226866166172286907691060333580739794735754141517928503510445368134531623057
c = 60939585660386801273264345336943282595466297131309357817378708003135300231065734017829038358019271553508356563122851120615655640023951268162873980957560729424913748657116293860815453225453706274388027182906741605930908510329721874004000783548599414462355143868922204060850666210978837231187722295496753756990

R.<x> = PolynomialRing(Zmod(n))
f = x + (peek<<240)
p = int(f.small_roots(X=2**240, beta=0.5, epsilon=1/35)[0] + (peek<<240))
q = n//p
d = pow(65537,-1,(p-1)*(q-1))
from Crypto.Util.number import long_to_bytes
long_to_bytes(int(pow(c, d, n)))
```

Flag: ```HCMUS-CTF{d0nt_b3_4n_3XhiB1ti0ni5t_0r_y0uLL_g3t_eXp0s3d}```

### 3. M side

Source:
```py
from Crypto.Util.number import getStrongPrime, bytes_to_long as b2l, isPrime
import os


FLAG = os.getenv('FLAG', 'FLAG{hue_hue_hue}').encode()
p = getStrongPrime(512)
q = getStrongPrime(512)
while not isPrime(4 * p * p + q * q):
    p = getStrongPrime(512)
    q = getStrongPrime(512)

hint = 4 * p * p + q * q 
e = 65537
print(f"hint: {hint}")
# n for wat?
print(f"ct: {pow(b2l(FLAG), e, p * q)}")

"""
hint: 461200758828450131454210143800752390120604788702850446626677508860195202567872951525840356360652411410325507978408159551511745286515952077623277648013847300682326320491554673107482337297490624180111664616997179295920679292302740410414234460216609334491960689077587284658443529175658488037725444342064697588997
ct: 8300471686897645926578017317669008715657023063758326776858584536715934138214945634323122846623068419230274473129224549308720801900902282047728570866212721492776095667521172972075671434379851908665193507551179353494082306227364627107561955072596424518466905164461036060360232934285662592773679335020824318918
"""
```

This challenge has an open vulnerability with the hint = 4p^2 + q^2 to find q and p. This is a special form of the Diophantine equation: given n = a^b + b^2, find a, b. There is an [online tool](https://www.alpertron.com.ar/GAUSSIAN.HTM) to solve this problem. Once 2p and q are known, the remaining task is simple.

```py
from Crypto.Util.number import isPrime, long_to_bytes

q = int('9513 749018 075983 034085 918764 185242 949986 187938 391728 694055 305209 717744 257503 225678 393636 438369 553095 045978 207938 932347 555839 964566 376496 993702 806422 385729'.replace(' ', ''))
p = int('19253 294223 314315 727716 037086 964210 594461 001022 934798 241434 958729 430216 563195 726834 194376 256655 558434 205505 701941 181260 137383 350002 506166 062809 813588 037666'.replace(' ', ''))
p = p//2

hint = 461200758828450131454210143800752390120604788702850446626677508860195202567872951525840356360652411410325507978408159551511745286515952077623277648013847300682326320491554673107482337297490624180111664616997179295920679292302740410414234460216609334491960689077587284658443529175658488037725444342064697588997
ct = 8300471686897645926578017317669008715657023063758326776858584536715934138214945634323122846623068419230274473129224549308720801900902282047728570866212721492776095667521172972075671434379851908665193507551179353494082306227364627107561955072596424518466905164461036060360232934285662592773679335020824318918
assert isPrime(q)
e = 65537
d = pow(e, -1, (p-1)*(q-1))
print(long_to_bytes(pow(ct, d, p*q)))
```

Flag: ```HCMUS-CTF{either_thu3_0r_3uclid_wh1ch3v3r_it_t4k35}```

### 4. Falsehood

Source:
```py
import os
import numpy as np
from sage.all import ComplexField, PolynomialRing
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
from binascii import hexlify

FLAG = os.getenv('FLAG', "FLAG{this is a real flag}")
bits = 1111
C = ComplexField(bits)
P = PolynomialRing(C, names='x')
(x,) = P.gens()

key_array = np.random.choice(256, size=(16,))
key = b''.join([int(i).to_bytes(1, 'big') for i in key_array])

f = sum([coeff * x**i for i, coeff in enumerate(key_array)])
hint = []
for _ in range(16):
    X = random.randint(10**8, 10**10)
    Y = int(abs(f(X)))
    while [X, Y] in hint:
        X = random.randint(10**8, 10**10)
        Y = int(abs(f(X)))
    hint.append([X, Y])


cip = AES.new(key, AES.MODE_CBC)
ct = cip.encrypt(pad(FLAG.encode(),16))
iv = cip.iv
with open('output.txt', 'w') as file:
    file.write(str(hint)+'\n')
    print(f"ct = {hexlify(ct).decode()}, iv = {hexlify(iv).decode()}", file=file)

```

The issue in this challenge is that it provides a 15th degree polynomial function f(x) with 16 coefficients and also gives 16 points (a, f(a)). Therefore, the task is to solve a system of equations to find the coefficients of the polynomial function, which can be done by using interpolation techniques.

```py
import os
import numpy as np
from sage.all import ComplexField, PolynomialRing
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
from binascii import hexlify

hint = eval(open('output.txt', 'r').readline().strip())
bits = 1111
C = ComplexField(bits)

A = []
b = []
for h in hint:
    b.append(C(h[1]))
    X = [C(h[0])^i for i in range(16)]
    A.append(X)
    


A = Matrix(C, A)
b = vector(C, b)

key_array = [(round(abs(i))) for i in A^-1*b]
key = b''.join([int(i).to_bytes(1, 'big') for i in key_array])
ct = 'be205fd34ebe59af55ea11fec9aea50197fbf35d5b52c650a6c9563186625e8b6021ba31db538fa4b60c69a42c96ee3bebaba53ac9afa9c3c185d4d0b145bc8251d892c243f1aa4037aeea003714e24c'
iv = '370abc6fce33f812de7b88daaa82e4c4'
ct = bytes.fromhex(ct)
iv = bytes.fromhex(iv)

cip = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
cip.decrypt(ct)
```

Flag: ```HCMUS-CTF{just_because_you're_correct_doesn't_mean_you're_right}```

### 5. Cry1

Source:
```py
import time
import random
import threading
import socketserver
import os

FLAG_FILE = os.getenv("FLAG", 'FLAG')
PORT = int(os.getenv("APP_PORT", 11111))
HOST = "0.0.0.0"

assert FLAG_FILE is not None, "Environment variable FLAG not set"
assert PORT is not None, "Environment variable APP_PORT not set"


class Service(socketserver.BaseRequestHandler):
    def handle(self):
        self.flag = self.get_flag()
        self.user_id = int(time.time())
        self.send(f"Welcome\n")
        assert len(self.flag) == 26
        self.send(
            f"Here is your encoded flag: {self.encode(self.flag, self.gen_key(self.user_id, len(self.flag)))}\n"
        )
        self.send(f'{self.gen_key(self.user_id, len(self.flag))}\n')

    def get_flag(self):
        with open(FLAG_FILE, "r") as f:
            return f.readline()

    def encode(self, data, key):
        return sum([a * ord(b) for a, b in zip(key, data)])

    def gen_key(self, user_id, n):
        random.seed(user_id)
        return [random.randrange(1024) for i in range(n)]

    def send(self, string: str):
        self.request.sendall(string.encode("utf-8"))

    def receive(self):
        return self.request.recv(1024).strip().decode("utf-8")


class ThreadedService(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer,
    socketserver.DatagramRequestHandler,
):
    pass


def main():
    service = Service
    server = ThreadedService((HOST, PORT), service)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("Server started on " + str(server.server_address) + "!")
    # Now let the main thread just wait...
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
```

The issue in this challenge is that it provides the dot product of the flag and a random vector generated from int(time.time()) and len_flag. It is quite difficult to solve with just one dot product. However, it is possible to connect to the server multiple times to create a system of equations (26 times). Solve the system to obtain the flag. Due to the difference in clock epoch between the client and server, the code may sometimes run and sometimes not run.

```py
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
```

Flag: ```HCMUS-CTF{the_EASIEST_0ne}```

### 6. Real key

Source:
```py
from Crypto.Cipher import AES
from Crypto.Util.number import getRandomInteger
from Crypto.Util.Padding import pad
import numpy as np




def gen_key():
    key = getRandomInteger(128).to_bytes(16, 'big')
    while b'\0' in key: key = getRandomInteger(128).to_bytes(16, 'big')
    mat = [[i for i in key[k:k+4]] for k in range(0, 16, 4)]
    return key, mat

def f(mat):
    """Make the key wavy"""
    N = 1600
    T = 1/800
    x = np.linspace(0, N*T, N)
    ys = [np.sum(np.array([.5**i * np.sin(n * 2 * np.pi * x) for i, n in enumerate(b)]), axis=0).tolist() for b in mat]
    return ys

def check_good_mat(mat):
    for row in mat:
        for i in range(4):
            if row[i] > 255: return False
            for j in range(i + 1, 4):
                if -1 == row[i] - row[j] or row[i] - row[j] == 1 or row[i] == row[j]: return False
    return True


def main():        
    key, mat = gen_key()
    while not check_good_mat(mat):
        key, mat = gen_key()

    ys = f(mat)
    FLAG = pad(b'FLAG{real_flag_goes_here}', 16)
    cip = AES.new(key, AES.MODE_CBC)
    iv = cip.iv

    ciphertext = cip.encrypt(FLAG)

    # The stuff which will be given
    with open('output.txt', 'w') as ofile:
        print(ys, file=ofile)
    with open('ciphertext.bin', 'wb') as ofile:
        ofile.write(iv)
        ofile.write(ciphertext)

if __name__ == '__main__':
    main()
```

The issue in this challenge is to find the vector x from the function f(x), where x is a 4-dimensional vector, and the value of f(vector) is given. This is a relatively simple task, and one can choose a random vector and use the differential method to optimize it to the nearest point. Running the algorithm several times will give the result.

```py
import numpy as np
from scipy.optimize import differential_evolution
from Crypto.Cipher import AES

def f(vec):
    """Make the key wavy"""
    N = 1600
    T = 1/800
    x = np.linspace(0, N*T, N)
    ys = np.sum(np.array([.5**i * np.sin(n * 2 * np.pi * x) for i, n in enumerate(vec)]), axis=0)
    return ys

def objective(vec, ys_desired):
    """Squared difference between f(vec) and ys_desired"""
    ys = f(vec)
    return np.sum((ys - ys_desired)**2)

def find_vec(ys_desired):
    """Find the 4-dimensional vector vec that produces f(vec) closest to ys_desired"""
    bounds = [(0, 255)]*4
    result = differential_evolution(objective, bounds, args=(ys_desired,))
    return result.x.astype(np.uint8)
        
if __name__ == '__main__':
    mat = []
    ys = eval(open('output.txt', 'r').read().strip())
    for i in range(4):
        while True:
            vec = find_vec(ys[i])
            if np.allclose(f(vec),  ys[i]):
                mat.append(list(vec))
                print(vec)
                break
    key = bytes(sum(mat, []))
    bin = open('ciphertext.bin', 'rb').read()
    iv = bin[:16]
    ct = bin[16:]
    cip = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    print(cip.decrypt(ct))

```

Flag: ```HCMUS-CTF{https://www.youtube.com/watch?v=nmgFG7PUHfo}```

## Crypto-RE

### 1. Is this Crypto?

This challenge prompts the user to input a name and a word, and uses S(name) as the key and M(word) as the IV to perform AES-CBC-256 encryption. The task is to find the key and IV. In the check function, there is a function s that stores two SHA224 hashes.

```py
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
```

I tried to crack the SHA224 hashes, and got "recis" and "cannibalization" as the name and word respectively. Now, the only thing left to do is to find out what the S and M functions do. After examining the constants used in these two functions and doing some Google search, I found out that S and M are SHA256 and MD5 functions respectively. Therefore, all that is needed is to connect again with the correct key and IV.

```py
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
```

Flag: ```HCMUS-CTF{r_u_ready_for_fREddy?}```
