# this is an extension of the implementation of the encryption and 
# decryption of the twofish algorithm in EBC and CBC (to be implemented) operation modes

# it utilizes the twofish v0.3.0 python module for its most basic
# block encryptions and decryptions 

from twofish import Twofish as tf

class TwoFish:
    def encryptEBC(key: str, plaintext: str):
        T = tf(str.encode(key))
        
        # pad the plaintext
        if len(plaintext) % 16:
            plaintext = plaintext + '%'*(16 - (len(plaintext) % 16))
        
        plaintext= str.encode(plaintext)
        ciphertext = b''

        for x in range(len(plaintext)//16):
            ciphertext += T.encrypt(plaintext[x * 16 : (x+1) * 16])
        
        return ciphertext

    def decryptEBC(key: str, ciphertext: bytes):
        T = tf(str.encode(key))

        plaintext = b''

        for x in range(len(ciphertext)//16):
            plaintext += T.decrypt(ciphertext[x * 16 : (x+1) * 16])

        # remove padding
        plaintext = plaintext.decode(errors="ignore").strip('%')

        return plaintext
