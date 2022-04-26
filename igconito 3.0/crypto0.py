import base64
with open("./README.md", 'r') as f:
    cipher = f.read().strip()

cipher = cipher.encode()
for i in range(17):
    cipher = base64.b64decode(cipher)
    
key = "this_key_is_a_bit_annoying>_<"
def xor(a, b):
    res = []
    for i, j in zip(a, b):
        res.append(i^j)
    return bytes(res)
print(xor(cipher, key.encode()).decode())