import hashlib

def generate_aes_key(username, password):
    # Concatenate the inputs
    input_str = username + password
    
    # Hash the concatenated string using SHA-256
    hash_obj = hashlib.sha256()
    hash_obj.update(input_str.encode())
    hash_digest = hash_obj.digest()
    
    # Truncate the hash to fit AES key size (128 bits or 16 bytes for AES-128)
    aes_key = hash_digest[:16]  # Adjust this if using AES-256 or other variants
    
    return aes_key