import random
import string

def generate_password(length=12):
    """Generate a random password with letters, digits, and special characters."""
    if length < 6:
        raise ValueError("Password length should be at least 6 characters.")
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

if __name__ == "__main__":
    try:
        length = int(input("Enter the desired password length (minimum 6): "))
        password = generate_password(length)
        print(f"Generated Password: {password}")
    except ValueError as e:
        print(f"Error: {e}")
