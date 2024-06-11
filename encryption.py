from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def encrypt_string(plain_text, key):
    # Generate a random 16-byte IV
    iv = os.urandom(16)
    
    # Create a cipher object
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the plain text to be multiple of block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()
    
    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted_data

def generate_key():
    # Generate a random 32-byte key (256-bit key)
    return os.urandom(32)


