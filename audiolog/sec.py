from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
def encrypt_audio_aes_gcm(input_file, output_file, password):
    with open(input_file, 'rb') as f:
        audio_data = f.read()

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)

    cipher = Cipher(algorithms.AES(key), modes.GCM(salt), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(audio_data) + encryptor.finalize()

    with open(output_file, 'wb') as f:
        f.write(salt + ciphertext + encryptor.tag)

def decrypt_audio_aes_gcm(input_file, output_file, password):
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    salt = encrypted_data[:16]
    ciphertext = encrypted_data[16:-16]
    tag = encrypted_data[-16:]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)

    cipher = Cipher(algorithms.AES(key), modes.GCM(salt, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)


