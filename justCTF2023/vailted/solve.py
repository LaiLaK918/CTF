from pwn import *
from coincurve import PrivateKey
import json

conn = remote('vaulted.nc.jctf.pro', 1337)

# Create a secret key
sk = PrivateKey(b'1234')
pk = sk.public_key

# Send the public key to the remote server
print(json.loads(conn.recvline().decode()))
conn.sendline(json.dumps({'method': 'enroll', 'pubkey': pk.format().hex()}).encode())

print(json.loads(conn.recvline().decode()))
# Sign message
sig = sk.sign(b'get_flag').hex()

# Create three signatures with compressed, uncompressed and hybrid format
pk1 = pk.format().hex()
pk2 = pk.format(compressed=False).hex()
pk3 = '06' + pk.format(compressed=False).hex()[2:]

conn.sendline(json.dumps({'method': 'get_flag', 'pubkeys': [pk1, pk2, pk3], 'signatures': [sig, sig, sig]}).encode())
print(json.loads(conn.recvline().decode()))
