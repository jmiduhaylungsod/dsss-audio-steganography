import numpy as np

def message_mix(L, bits, lower=-1, upper=1, K=0):
    N = bits.size
    m_sig = np.repeat(bits, L)
    m_sig = (m_sig * (upper - lower)) + lower

    return m_sig