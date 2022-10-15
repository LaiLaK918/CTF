from pwn import remote

HOST, PORT = '65.21.255.31', 32066

io = remote(HOST, PORT)
STEP = 40
for i in range(5):
    print(io.recvline())
for i in range(STEP):
    p_raw = io.recvline()
    p = p_raw[6:-1].strip()
    p = int(p)
    q_raw = io.recvline()
    q = q_raw[6:-1].strip()
    g = int(q)
    io.sendlineafter(b'Send the solution x = ', str(1-p).encode())
    print(io.recvline())
    print(io.recvline())

