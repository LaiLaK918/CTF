#!/bin/sage

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
