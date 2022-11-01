#!/usr/bin/env python3


from pwn import remote

def swap(s):
    l = len(s)//4
    return s[l:2*l] + s[:l] + s[3*l:] + s[2*l:3*l]

io = remote('flu.xxx', 12001)

ct = open('./src/encrypted_flag.txt', 'r').read().strip()

io.sendline(swap(ct).encode())

io.recvline()
pt = swap(io.recv().strip().decode()[-64:])

print(f'Flag: {bytes.fromhex(pt).decode()}')
