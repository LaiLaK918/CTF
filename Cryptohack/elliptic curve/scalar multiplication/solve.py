from Crypto.Util.number import inverse


# from previous challenge (assumed prerequisite)
def pt_add(p, q, E):
    zero = (0, 0)
    if p == zero:
        return q
    elif q == zero:
        return p
    else:
        x1, y1 = p
        x2, y2 = q
        if x1 == x2 and y1 == -y2:
            return zero

        Ea, Ep = E['a'], E['p']
        if p != q:
            lmd = (y2 - y1) * inverse(x2 - x1, Ep)
        else:
            lmd = (3 * (x1**2) + Ea) * inverse(2 * y1, Ep)
        x3 = ((lmd**2) - x1 - x2) % Ep
        y3 = (lmd * (x1 - x3) - y1) % Ep
        return x3, y3


def scalar_mult(n, p, E):
    q, r = p, (0, 0)
    while n > 0:
        if n % 2 == 1:
            r = pt_add(r, q, E)
        q = pt_add(q, q, E)
        n //= 2
    return r


# expect to create a module of helper functions in this file
if __name__ == '__main__':
    E = {'a': 497, 'b': 1768, 'p': 9739}

    # previous challenge assertions omitted for brevity

    x = (5323, 5438)
    assert scalar_mult(1337, x, E) == (1089, 6931)

    p = (2339, 2213)
    q = scalar_mult(7863, p, E)
    x1, y1 = q
    assert x1 in range(E['p'])
    assert y1 in range(E['p'])
    print('mult: ' + 'crypto{' + str(x1) + ',' + str(y1) + '}')
