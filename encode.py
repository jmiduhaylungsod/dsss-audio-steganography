
import numpy as np
from two_fish import TwoFish as tf
from mixer import message_mix
from logistic import logistic_prng


def message_encode(text, audio_data, password):
    min_SegLength = 1024
    # if there is a password, encrypt plaintext using twofish
    if password:
        bytestring = tf.encryptEBC(password, text)
        bitstring = ''.join(format(byte, '08b') for byte in bytestring)
        key = len(bytestring)
    # else, no encryption
    else:
        bitstring = ''.join(format(ord(char), '08b') for char in text)
        key = len(text)
    
    bits = np.array(list(bitstring), 'uint8')

    calc_SegLength = len(audio_data)//bits.size 
    segLength = max(min_SegLength, calc_SegLength)
    nframe = len(audio_data)//segLength
    N = nframe - (nframe%8)

    if bits.size > N:
        print("Message too long. Will now be cropped...")
        bits = bits[0:N]

    # ----use pseudo random chip code generator with input for r----
    if password:
        r = logistic_prng(password, segLength)
    
    # ----array of ones for r
    else:
        r = np.ones(segLength, 'u1')

    
    pr = np.tile(r, N)
    alpha = 0.005
    # -------embedding-------
    mix = message_mix(segLength, bits)
    stego = np.copy(audio_data)
    apr = alpha * pr
    power = set_power(audio_data, N, segLength, r, alpha)
    stego[:mix.size] += mix * power * apr
    # -----------------------
    
    return stego, key

# chip code generator
def prng(key, L):
    password = np.fromstring(key,dtype='B')
    range = np.arange(1,password.size+1)
    gen_seed = np.sum(np.multiply(password,range))
    rng = np.random.default_rng(gen_seed)
    out = rng.choice([1,-1], L)

    return out

# adjusts embedding level according to the 
# segment's sum, normalized to alpha's sum 
# to ensure that correct bit is retrieved
def set_power(audio_data, N, L, r, alpha):
    powers = np.ones(N*L, 'f8')

    for x in range(N):
        power = (np.sum(audio_data[x*L : (x+1)*L] * r)) / (L*alpha)
        if abs(power) >= 0.9:
            powers[x*L : (x+1)*L] = abs(power) + 0.5
    return powers
        