import os

from numpy import block


with open('encrypted_messages.txt', 'r') as f:
    SUPER_SECRET_MESSAGES = [msg.strip() for msg in f.readlines()]


def deriveKey(key):
    derived_key = []

    for i, char in enumerate(key):
        previous_letters = key[:i]
        new_number = 1
        for j, previous_char in enumerate(previous_letters):
            if previous_char > char:
                derived_key[j] += 1
            else:
                new_number += 1
        derived_key.append(new_number)
    return derived_key


def transpose(array):
    print(*array)
    return [row for row in map(list, zip(*array))]

def detranspose(array, key):
    r = len(array) // len(key)
    res = []
    for i in range(0, len(array), r):
        res.append(list(array[i:i+r]))
    return res

def flatten(array):
    return "".join([i for sub in array for i in sub])

def deflatten(array):
    res = ""
    print(*array)
    for i in range(len(array[0])):
        for j in range(len(array)):
            res += array[j][i]
            
    return res

def twistedColumnarDecrypt(ct, key):
    derived_key = deriveKey(key)
    print(f"derived key = {derived_key}")
    width = len(key)
    print(f"width = {width}")
    print(f"ciphertext = '{ct}'")
    # blocks = [pt[i:i + width] for i in range(0, len(pt), width)]
    blocks = ct
    print(f"blocks before detranspose: {blocks}")
    blocks = detranspose(blocks, key)        
    print(f"blocks after detranspose: {blocks}")
    # pt = [blocks[derived_key.index(i - 1)][::-1] for i in range(width, 1, -1)]
    pt = [[] for i in range(len(key))]
    for i in range(width - 1, -1, -1):
        index = derived_key.index(i + 1)
        pt[index] = blocks[-1][::-1]
        blocks.pop()
        print(f"pt = {pt} with i = {i}, index = {index}")
    pt = deflatten(pt)
    print(f"plaintext = {pt}")
    return pt



class PRNG:   # Zp
    def __init__(self, seed):
        self.p = 0x2ea250216d705
        self.a = self.p
        self.b = int.from_bytes(os.urandom(16), 'big')
        self.rn = seed

    def next(self):
        self.rn = ((self.a * self.rn) + self.b) % self.p
        return self.rn


def main():
    key = '729513912306026'
    pts = ""
    with open('encrypted_messages.txt', 'r') as f:
        ctt = [msg.strip() for msg in f.readlines()]
        for mess in ctt:
            pt = twistedColumnarDecrypt(mess, key)
            pts += pt + '\n'

    with open('pt.txt', 'w') as f:
        f.write(pts)

if __name__ == '__main__':
    main()
