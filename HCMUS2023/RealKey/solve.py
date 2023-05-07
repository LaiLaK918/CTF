import numpy as np
from scipy.optimize import differential_evolution
from Crypto.Cipher import AES

def f(vec):
    """Make the key wavy"""
    N = 1600
    T = 1/800
    x = np.linspace(0, N*T, N)
    ys = np.sum(np.array([.5**i * np.sin(n * 2 * np.pi * x) for i, n in enumerate(vec)]), axis=0)
    return ys

def objective(vec, ys_desired):
    """Squared difference between f(vec) and ys_desired"""
    ys = f(vec)
    return np.sum((ys - ys_desired)**2)

def find_vec(ys_desired):
    """Find the 4-dimensional vector vec that produces f(vec) closest to ys_desired"""
    bounds = [(0, 255)]*4
    result = differential_evolution(objective, bounds, args=(ys_desired,))
    return result.x.astype(np.uint8)
        
if __name__ == '__main__':
    mat = []
    ys = eval(open('output.txt', 'r').read().strip())
    for i in range(4):
        while True:
            vec = find_vec(ys[i])
            if np.allclose(f(vec),  ys[i]):
                mat.append(list(vec))
                print(vec)
                break
    key = bytes(sum(mat, []))
    bin = open('ciphertext.bin', 'rb').read()
    iv = bin[:16]
    ct = bin[16:]
    cip = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    print(cip.decrypt(ct))

    