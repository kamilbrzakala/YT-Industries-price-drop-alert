from cryptography.fernet import Fernet
import os

# Generate a key
def generate_key():
    key = Fernet.generate_key()
    with open("C:\\Users\\xxx\\key.txt", "wb") as key_file:
        key_file.write(key)

# Load the key
def load_key():
    return open("key.txt", "rb").read()

# Encrypt the password
def encrypt_password(password):
    key = load_key()
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

# Decrypt the password
def decrypt_password(encrypted_password):
    key = load_key()
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

# Generate and save the key
generate_key()

# Encrypt the password and save it
#password = "!"  # Replace with your actual email password
encrypted_password = encrypt_password(password)
with open("C:\\Users\\xxx\\encrypted_password.txt", "wb") as password_file:
    password_file.write(encrypted_password)

# Decrypt the password
with open("C:\\Users\\xxx\\encrypted_password.txt", "rb") as password_file:
    encrypted_password = password_file.read()
decrypted_password = decrypt_password(encrypted_password)

print("Original password:", password)
print("Decrypted password:", decrypted_password)