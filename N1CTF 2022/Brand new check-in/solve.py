from ast import literal_eval
from Crypto.Util.number import *
from tqdm import tqdm

lines = open("./src/output.txt","r").readlines()
s,t,n = literal_eval(lines[0].strip())
enc = literal_eval(lines[1])

def xgcd(a: int, b: int):
    x0, y0, x1, y1 = 0, 1, 1, 0
    while a != 0:
        q, a, b = b // a, b % a, a
        x0, x1 = x1, x0 - x1 * q
        y0, y1 = y1, y0 - y1 * q
    return b, x0, y0

encflag = b""
r_list = []

for c1, c2 in tqdm(enc):
    if c1 == 0 and c2 == 0:
        # m is zero , r unknown, set -1
        encflag += bytes([0])
        r_list.append(-1)
        continue
    for m in range(256):
        g, x, y = xgcd(s, t)
        z = pow(c1, x, n)
        w = pow(c2, y, n)
        mm = pow(m, -(x+y), n)
        r_ = mm * z * w % n
        c1_ = (m * pow(r_, s // g, n)) % n
        c2_ = (m * pow(r_, t // g, n)) % n
        if c1_ == c1 and c2_ == c2:
            encflag += bytes([m])
            r_list.append(r_)
            break
print(encflag)

# Initialise rng (random.getrandbits)
import random
import time
import copy
from sympy import prod
from Crypto.Util.number import *
from ast import literal_eval
from tqdm import tqdm
from mt19937predictor import MT19937Predictor

off = 48
lines = open("./src/output.txt","r").readlines()
s,t,n = literal_eval(lines[0].strip())
enc = literal_eval(lines[1])

r = r_list # above r_list

data = r[off:20+off] 
multi_r_list = []

def split32bit(d):
    temp = []
    for _ in range(1024//32):
        temp.append(d%2**32)
        d = d>>32
    assert d==0
    return temp
    
for d in data[:20]:
    assert d < n
    multi_ls = [split32bit(d)]
    while d + n < 2**1024:
        d = d + n
        multi_ls.append(split32bit(d))
    multi_r_list.append(multi_ls)
    
from itertools import product
brute_length = prod([len(i) for i in multi_r_list])
print(f"[+] Brute forcing space {brute_length} {brute_length.bit_length()}")

# split the brute-forcing space
expand_part = product(*(multi_r_list[-3:]))
brute_list = [product(*(multi_r_list[:-3]+[[f[0]],[f[1]],[f[2]]])) for f in expand_part]
n_cores = len(brute_list)
n_cores = 4
slice_length = brute_length//n_cores
datas = [[b] for b in brute_list]
print(f"[+] cores {n_cores}")

def verify_func(brute_list):
    for i in tqdm(brute_list,total=slice_length):
        MT_data = []
        for ls in i:
            MT_data.extend(ls)
        predictor = MT19937Predictor()
        for _ in range(624):
            predictor.setrandbits(MT_data[_], 32)
            
        mflag = True
        for _ in range(640-624):
            if predictor.getrandbits(32)!= MT_data[624 + _]:
                mflag = False
                break
        if mflag == False:
            continue
        # print(f"[+] possible result : {MT_data}")
        for _ in range(20):
            if predictor.getrandbits(1024)%n != r[20+off+_]:
                mflag = False
                break
        if mflag == False:
            continue
        print(f"[+] GOOD MT STATE")
        return (True,MT_data[:])
    return (False,[])
    
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import os


def parallel_process(array, function, use_kwargs=False):
    """
        A parallel version of the map function with a progress bar. 

        Args:
            array (array-like): An array to iterate over.
            function (function): A python function to apply to the elements of array
            n_jobs (int, default=16): The number of cores to use
            use_kwargs (boolean, default=False): Whether to consider the elements of array as dictionaries of 
                keyword arguments to function 
            front_num (int, default=3): The number of iterations to run serially before kicking off the parallel job. 
                Useful for catching bugs
        Returns:
            [function(array[0]), function(array[1]), ...]
    """
    front = []
    n_jobs = n_cores
    with ProcessPoolExecutor(max_workers=n_jobs) as pool:
        if use_kwargs:
            futures = [pool.submit(function, **a) for a in array]
        else:
            futures = [pool.submit(function, *a) for a in array]
        kwargs = {
            'total': len(futures),
            'unit': 'it',
            'unit_scale': True,
            'leave': True
        }
        #Print out the progress as tasks complete
        for f in tqdm(as_completed(futures), **kwargs):
            res = f.result()
            if res[0] == True:
                print("[+] find!")
                print(res)
                pool.shutdown(wait=True, cancel_futures=True)
                break
    return res

res_list = parallel_process(datas,verify_func)
data = res_list # results from above MT state
import random
from Crypto.Util.number import *
from ast import literal_eval
from tqdm import tqdm

lines = open("./src/output.txt","r").readlines()
s,t,n = literal_eval(lines[0].strip())
enc = literal_eval(lines[1])

# https://github.com/JuliaPoo/MT19937-Symbolic-Execution-and-Solver
import sys
sys.path.append('./src/source')
# Import symbolic execution
from MT19937 import MT19937, MT19937_symbolic
# Import XorSolver
from XorSolver import XorSolver
rng = lambda: random.getrandbits(1024)

rng_clone = MT19937(state_from_data = (data, 32))
shift = 64*(1024//32)
rng_clone.reverse_states(shift)

def get1024():
    res = 0 
    temps = []
    for i in range(32):
        temps.append(rng_clone())
    for num in temps[::-1]:
        res = (res<<32) + num
    return res


res_ls = []
for _ in range(64):
    rnd_num = get1024()
    res_ls.append(rnd_num)
    if rnd_num%n == s%n:
        print("[+] cracked")
        a = res_ls[-2]
        break
        
kphi = s*a+(1-a)*t
print(f"[+] kphi found , verify {pow(2,kphi,n) == 1} ")
encflag = b'\x08EZg\xbf\xa0\xeb\x9d\x81\x01\xa8\x96m\x97\x08I(\xed\xb5iQE\xdb\xf5\x8c\xbdcr!\xe6\xc9\xac\x0c\x16K\xa0\x0fr\xecM\x04\xe6\x87\x0f}9\x94\xcfa\x16\x87\x8f4\xcd\xcb\xa4\x0eq\xc3Q\x16\x928&\xe2\x18C\xafN\x87\xcc\x18\xc2D\x9d\x06\xbd"\xe7\xe8\xb7\x12\xb0\xb8CC\x9aM\xff\x12\x00\x05,\xeeopYC)mI\xb7\x81\xb6\x13\x0e\x8a\xc0\xd7\xd3\xd2\xa9\xe5vg.\xa4\xf3\xaa\x10f\x9c\xa4nS=O\xe9'
encnum = bytes_to_long(encflag)
d = inverse(0x10001,kphi)
m = long_to_bytes(pow(encnum,d,n))
print(m)
