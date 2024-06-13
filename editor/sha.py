import hashlib

def hash_password(password):
    # Encode the password string into bytes
    password_bytes = password.encode('utf-8')
    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    return hashed_password

def check_password(input_password, hashed_password):
    # Hash the input password to compare it with the hashed password
    input_hashed_password = hash_password(input_password)
    # Compare the two hashed passwords
    if input_hashed_password == hashed_password:
        return True
    else:
        return False

