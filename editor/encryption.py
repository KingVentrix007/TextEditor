import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend


def encrypt_string(plain_text, key):
    # Generate a random 12-byte nonce (IV)
    nonce = os.urandom(12)
    
    # Create AESGCM object
    aesgcm = AESGCM(key)
    
    # Encrypt the plain text
    encrypted_data = aesgcm.encrypt(nonce, plain_text.encode(), None)
    
    return nonce + encrypted_data

def generate_key():
    # Generate a random 32-byte key (256-bit key)
    return AESGCM.generate_key(bit_length=256)


#Made encryption more secure