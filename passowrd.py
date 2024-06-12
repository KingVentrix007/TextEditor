from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    length=12,      # minimum length: 12 characters
    uppercase=2,    # require at least 2 uppercase letters
    numbers=2,      # require at least 2 digits
    special=2,      # require at least 2 special characters
)


def check_policy(password):
    if policy.test(password):
        return True
    else:
        return False
        # print("Password does not meet the strength requirements.")

def pawned_password(password):
    with open("./invalid_passwords.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        if password in lines:
            return False
    return True

def test_password(password):
    if(password == ""):
        return False
    policy_ = check_policy(password)
    pawned = pawned_password(password)
    if(policy_ == pawned):
        print(pawned)
        return pawned
    elif(policy_ != pawned):
        return False
    else:
        return False
