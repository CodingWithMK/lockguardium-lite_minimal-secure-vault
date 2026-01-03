import secrets
import string

def generate_password(length: int = 12,
                      use_uppercase=True,
                      use_lowercase=True,
                      use_digits=True,
                      use_special_chars=True
                      ) -> str:
    """
    Generates a random secure password.
    
    Parameter:
        length (int): Length of the password

    Returns:
        str: Random generated password 
    """

    # Defining character sets
    uppercase = string.ascii_uppercase if use_uppercase else ""
    lowercase = string.ascii_lowercase if use_lowercase else ""
    digits = string.digits if use_digits else ""
    punctuation = string.punctuation if use_special_chars else ""

    characteristics = (lowercase + uppercase + digits + punctuation)

    # Validate that at least one character set is selected
    if not characteristics:
        raise ValueError("At least one character set must be selected.")
    
    # Ensure password meets minimum criteria
    # generated_password = []
    custom_password = []

    # for _ in range(length):
    #     generated_password.append(secrets.choice(characteristics))
    # return "".join(generated_password)

    for _ in range(length):
        if use_uppercase and uppercase:
            custom_password.append(secrets.choice(uppercase))
        if use_lowercase and lowercase:
            custom_password.append(secrets.choice(lowercase))
        if use_digits and digits:
            custom_password.append(secrets.choice(digits))
        if use_special_chars and punctuation:
            custom_password.append(secrets.choice(punctuation))

    return "".join(custom_password)

if __name__ == "__main__":
    print(generate_password(use_lowercase=True, use_uppercase=True, use_digits=True, use_special_chars=True))
    assert generate_password(use_lowercase=True, use_uppercase=True, use_digits=True, use_special_chars=True)