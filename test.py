from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from cryptography.fernet import Fernet
# Generate a key from data

def generate_key_from_data(data):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'some_salt',  # Use a unique salt for each key
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(data.encode()))
    return key
# Encrypt data with the key
def encrypt_data(data, key):
    cipher = Fernet(key)
    if isinstance(data, str):
        data = data.encode()
    return cipher.encrypt(data)

# Decrypt data with the key
def decrypt_data(data, key):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(data)
    return decrypted_data.decode()

def cyclic_encrypt_data(data,key_prompt):
    key = generate_key_from_data(key_prompt)
    previous_data = data
    for _ in range(25):
        # print("Encryption Iteration ",_)
        encrypted_data = encrypt_data(previous_data, key)
        
        # print("Encrypted data:", encrypted_data)
        previous_data = encrypted_data
    return previous_data

def cyclic_decrypt_data(data,key_prompt):
    previous_data = data
    key = generate_key_from_data(key_prompt)
    for _ in range(25):
        # print("Decryption Iteration ",_)
        decrypted_data = decrypt_data(previous_data, key)
        previous_data = decrypted_data
    print("Decrypted data:", decrypted_data)
# Example usage
def main():
    initial_data = input("Enter initial data: ")
    key = generate_key_from_data(initial_data)
    previous_data = initial_data
    for _ in range(25):
        # print("Encryption Iteration ",_)
        encrypted_data = encrypt_data(previous_data, key)
        
        # print("Encrypted data:", encrypted_data)
        previous_data = encrypted_data

    # previous_data = input("Enter initial encrypted data: ")
    for _ in range(25):
        # print("Decryption Iteration ",_)
        decrypted_data = decrypt_data(previous_data, key)
        previous_data = decrypted_data
    print("Decrypted data:", decrypted_data)

if __name__ == "__main__":
    main()
