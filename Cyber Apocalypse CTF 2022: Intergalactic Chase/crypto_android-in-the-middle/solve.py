m = b"Initialization Sequence - Code 0"
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long

def encrypt(encrypted, shared_secret):
    key = hashlib.md5(long_to_bytes(shared_secret)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    message = cipher.encrypt(encrypted)
    return message

print(hex(bytes_to_long(encrypt(m, 0)))[2:])
