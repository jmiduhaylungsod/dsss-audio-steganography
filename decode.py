import numpy as np
from two_fish import TwoFish as tf
from logistic import logistic_prng


def message_decode(audio_data, password, N):
    min_SegLength = 1024

    calc_SegLength = len(audio_data)//N
    segLength = max(min_SegLength, calc_SegLength)
    nframe = len(audio_data)//segLength
    N = nframe - (nframe%8)

    x_sig = np.reshape(audio_data[:N*segLength], (N, segLength))

    # ----use pseudo random chip code generator with input for r----
    if password:
        r = logistic_prng(password, segLength)
    
    # ----array of ones for r
    else:
        r = np.ones(segLength, 'u1')
    # ----array of ones for r

    bits = np.ones(N, dtype='int8')
    
    for i in range(N):
        c = np.sum(np.multiply(x_sig[i], r))
        if c < 0:
            bits[i] = 0
        else:
            bits[i] = 1

    chars = np.packbits(bits)  
    if password:
        bytestring = bytes(chars)
        out = tf.decryptEBC(password, bytestring)
    else:
        out = ''.join(chr(i) if i>0 and i<127 else "*" for i in chars)
    return out



def prng(key, L):
    password = np.fromstring(key,dtype='B')
    range = np.arange(1,password.size+1)
    gen_seed = np.sum(np.multiply(password,range))
    rng = np.random.default_rng(gen_seed)
    out = rng.choice([1,-1], L)
    return out
    