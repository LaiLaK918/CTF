from hashlib import sha256
from Crypto.Util.number import long_to_bytes,bytes_to_long
from Crypto.Cipher import AES
from pwn import *
BLOCK_SIZE = 32
def decrypt_block(block,secret):
    dec_block = b''
    for i, j in zip(block, secret):
        val = (i - j + 256)%256
        dec_block += bytes([val])
    return dec_block

def decrypt(enc, password):
    h = password
    blocks = [enc[i : i + BLOCK_SIZE] for i in range(0, len(enc), BLOCK_SIZE)]
    dec = b''
    for block in blocks:
        dec_block = decrypt_block(block, h)
        h = sha256(block + dec_block).digest()
        dec += dec_block
    return dec

HOST, POST = ??, ??
s = remote(HOST, PORT)
s.sendlineafter(b'> ', b'cat secret.txt')

msg = s.recv(4096).decode()
print(msg)
print(len(msg)%32)
enc  = bytes.fromhex(msg)
first_block = b'Command executed: cat secret.txt'
password = decrypt_block(enc[:32], first_block)
print(decrypt(enc, password))
