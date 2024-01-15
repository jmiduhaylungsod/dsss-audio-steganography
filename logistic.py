import numpy as np

def logistic_prng(key, L):
    out = np.ones(L, 'i4')
    password = np.frombuffer(key.encode(), 'B')
    max = 128 * password.size
    seed = 1-np.sum(password)/max

    # feed seed to logistic equation to get initial value
    x = 4 * seed * (1-seed)
    for i in range(L - 1):
        if x > 0.5:
            out[i] = 1
        else:
            out[i] = -1
        x = 4 * x * (1-x)
    
    return out


