import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
def decrypt_string(encrypted_data, key):
    # Extract the nonce from the beginning of the encrypted data
    nonce = encrypted_data[:12]
    
    # Extract the actual encrypted data
    ciphertext = encrypted_data[12:]
    
    # Create AESGCM object
    aesgcm = AESGCM(key)
    
    # Decrypt the data
    decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
    
    # Return the decrypted plain text
    return decrypted_data.decode()