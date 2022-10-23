#!/usr/bin/env python3

def find(idx, lowP, highP, lowQ, highQ, xor, n, NBITS):

    if idx == NBITS:
        assert highP * highQ == n
        print("FOUND!")
        print(highP)
        print(highQ)
        exit()


    highX = (xor >> (NBITS - 1 -idx)) & 1
    lowX = (xor >> idx) & 1

    possibleLow = []
    possibleHigh = []
    
    # find possible (highP, lowQ) pairs from the MSB of the XOR
    if highX == 1:
        possibleHigh.append(((highP << 1) | 1, lowQ))
        possibleHigh.append((highP << 1, lowQ + (1 << idx)))
    else:
        possibleHigh.append((highP << 1, lowQ))
        possibleHigh.append(((highP << 1) | 1, lowQ + (1 << idx)))
    
    # find possible (lowP, highQ) pairs from the LSB of the XOR
    if lowX == 1:
        possibleLow.append((lowP, (highQ << 1) | 1))
        possibleLow.append((lowP + (1 << idx), highQ << 1))
    else:
        possibleLow.append((lowP, highQ << 1))
        possibleLow.append((lowP + (1 << idx), (highQ << 1) | 1))


    for highP, lowQ in possibleHigh:
        for lowP, highQ in possibleLow:
            # prune lower bits
            if lowP * lowQ % (1 << (idx + 1)) != n % (1 << (idx + 1)):
                continue
            
            pad = NBITS-1-idx

            # check upper bit bounds
            if (highP << pad) * (highQ << pad) > n:
                continue

            if ((highP << pad) + (1 << pad) - 1) * ((highQ << pad) + (1 << pad) - 1) < n:
                continue

            find(idx+1, lowP, highP, lowQ, highQ, xor, n, NBITS)

def xor_factor(n, p_xor_q, prime_bits):
    find(0, 0, 0, 0, 0, p_xor_q, n, prime_bits)
    
if __name__ == '__main__':
    # test params

    NBITS = 512
    n = 153342396916538105228389844604657707491428056788672847550697727306332965113688161734184928502340063389805944751606853233980691631740462201365232680640173140929264281005775085463371950848223467977601447652530169573444881112823791610262204408257868244728097216834146410851717107402761308983285697611182983074893
    xor = 3551084838077090433831900645555386063043442912976229080632434410289074664593196489335469532063370582988952492150862930160920594215273070573601780382407014

    xor_factor(n, xor, NBITS)