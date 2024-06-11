from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64

# Define key and IV generation functions
def generate_key_iv(password: str, salt: bytes):
    # Derive key and IV from password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32 + 16,  # 32 bytes for the key, 16 bytes for the IV
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key_iv = kdf.derive(password.encode('utf-8'))
    return key_iv[:32], key_iv[32:]  # Return key and IV separately

def encrypt_filename(filename: str, password: str) -> str:
    if '.' in filename:
        name, ext = filename.rsplit('.', 1)
        ext = '.' + ext
    else:
        name, ext = filename, ''
    
    salt = os.urandom(16)  # Generate a random salt
    key, iv = generate_key_iv(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(name.encode('utf-8')) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    encoded_data = base64.urlsafe_b64encode(salt + encrypted_data).decode('utf-8')
    return f"{encoded_data}{ext}"

def decrypt_filename(encrypted_filename: str, password: str) -> str:
    if '.' in encrypted_filename:
        encoded_data, ext = encrypted_filename.rsplit('.', 1)
        ext = '.' + ext
    else:
        encoded_data, ext = encrypted_filename, ''
    
    data = base64.urlsafe_b64decode(encoded_data)
    salt = data[:16]
    encrypted_data = data[16:]
    key, iv = generate_key_iv(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data.decode('utf-8') + ext

def main():
    # Example usage
    password = "strong_password"
    original_filename = "example_file.enc"
    encrypted_filename = encrypt_filename(original_filename, password)
    print(f"Encrypted: {encrypted_filename}")

    decrypted_filename = decrypt_filename(encrypted_filename, password)
    print(f"Decrypted: {decrypted_filename}")

if __name__ == "__main__":
    main()
