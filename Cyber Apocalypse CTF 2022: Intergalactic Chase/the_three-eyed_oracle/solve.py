from Crypto.Util.number import long_to_bytes,bytes_to_long
from Crypto.Cipher import AES
from pwn import *
from string import printable
s = remote('46.101.25.63',30565)
FLAG = b''
def send_payload(payload):
    print(s.recvuntil(b'> ').decode())
    s.sendline(payload)

def get_flag():
    global FLAG
    Len = 35
    while not(b'HTB' in FLAG and b'}' in FLAG):
        
        payload = b'A'*(Len - len(FLAG))
        send_payload(payload.hex().encode())
        pattern = s.recvline().decode()
        print(pattern)
        pattern = bytes.fromhex(pattern)
        #test key
        for i in printable:
            print('testing ',i)
            payload = b'A'*(Len - len(FLAG)) + FLAG + i.encode()
            send_payload(payload.hex().encode())
            msg_recv =bytes.fromhex( s.recvline().decode())
            if msg_recv[32 : 48] == pattern[32 : 48]:
                FLAG += i.encode()
                break
        print(FLAG)

get_flag()
