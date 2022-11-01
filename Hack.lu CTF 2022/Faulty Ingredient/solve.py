from src.fluxtagram_leak1 import gf_mul123, sbox
from src.out import ct, ft, enc_flag
import aeskeyschedule as aks
from Crypto.Cipher import AES


def gen_fault_pos():
    s1_set = set()
    for fault_ind in range(4):
        for j in range(256):
            e = [0]*fault_ind + [j] + [0]*(3 - fault_ind)
            state_e = [0, 0, 0, 0]
            state_e[0] = gf_mul123(e[0], 2) ^ gf_mul123(e[1], 3) ^ gf_mul123(e[2], 1) ^ gf_mul123(e[3], 1)
            state_e[1] = gf_mul123(e[0], 1) ^ gf_mul123(e[1], 2) ^ gf_mul123(e[2], 3) ^ gf_mul123(e[3], 1)
            state_e[2] = gf_mul123(e[0], 1) ^ gf_mul123(e[1], 1) ^ gf_mul123(e[2], 2) ^ gf_mul123(e[3], 3)
            state_e[3] = gf_mul123(e[0], 3) ^ gf_mul123(e[1], 1) ^ gf_mul123(e[2], 1) ^ gf_mul123(e[3], 2)
            s1_set.add(tuple(state_e))
    return s1_set
        
def key_cands(ct, ft, s1_set, column=0):
    if column == 0:
        indexes = [0, 13, 10, 7]
    elif column == 1:
        indexes = [4, 1, 14, 11]
    elif column == 2:
        indexes = [8, 5, 2, 15]
    elif column == 3:
        indexes = [12, 9, 6, 3]
    e_dash_dash = [ft[ind] ^ ct[ind] for ind in indexes]

    i_set = set()

    for e_tup in s1_set:
        for i1 in range(256):
            if sbox[i1] ^ sbox[i1 ^ e_tup[0]] == e_dash_dash[0]:
                for i2 in range(256):
                    if sbox[i2] ^ sbox[i2 ^ e_tup[1]] == e_dash_dash[1]:
                        for i3 in range(256):
                            if sbox[i3] ^ sbox[i3 ^ e_tup[2]] == e_dash_dash[2]:
                                for i4 in range(256):
                                    if sbox[i4] ^ sbox[i4 ^ e_tup[3]] == e_dash_dash[3]:
                                        i_set.add((i1, i2, i3, i4))

    round_key_cands = set()
    for i_cand in i_set:
        round_key_cands.add(tuple(sbox[i_cand[i]] ^ ct[indexes[i]] for i in range(4)))
    return round_key_cands, indexes


def dfa(cts, fts, fault_columns=[0, 1, 2, 3]):
    s1_set = gen_fault_pos()
    round_10_key = [0]*16
    for column in fault_columns:
        all_round_key = []
        for ct, ft in zip(cts, fts):
            round_key_cands, indexes = key_cands(ct, ft, s1_set, column)
            all_round_key.append(round_key_cands)
        round_key = all_round_key[0]
        for i in range(1, len(cts)):
            round_key &= all_round_key[i]
        round_key = list(round_key)[0]
        for idx, val in zip(indexes, round_key):
            round_10_key[idx] = val
    return aks.reverse_key_schedule(bytes(round_10_key), 10)


def main():
    cts = [ct[i] for i in range(2)]
    fts = [ft[i] for i in range(2)]
    key = dfa(cts, fts)
    cipher = AES.new(key, AES.MODE_ECB)
    print(cipher.decrypt(bytes(enc_flag)).decode())
    

if __name__ == '__main__':
    main()
    