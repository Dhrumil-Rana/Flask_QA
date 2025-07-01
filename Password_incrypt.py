import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

if __name__ == "__main__":
    # Example usage
    input_password = input("Enter a password to hash: ")
    password = input_password.strip()
    hashed_password = hash_password(password)
    print(f"Original Password: {password}")
    print(f"Hashed Password: {hashed_password}")
