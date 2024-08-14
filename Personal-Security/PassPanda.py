'''WORK IN PROGRESS'''

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import base64
import hashlib
import os
import sqlite3
from getpass import getpass

# Generate a key for encrypting the database
def generate_db_key(master_password):
    digest = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

# Encrypt the database file
def encrypt_db(file_path, key):
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted_data = cipher_suite.encrypt(data)
    with open(file_path + '.enc', 'wb') as f:
        f.write(encrypted_data)
    os.remove(file_path)

# Decrypt the database file
def decrypt_db(file_path, key):
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    with open(file_path[:-4], 'wb') as f:
        f.write(decrypted_data)
    os.remove(file_path)

# Secure directory in the user's home directory
secure_dir = os.path.join(os.path.expanduser("~"), ".secure")
os.makedirs(secure_dir, exist_ok=True)  # Create directory if it does not exist

# Path to the database file
db_path = os.path.join(secure_dir, 'passwords.db')
encrypted_db_path = db_path + '.enc'

# Generate a key from the master password
def generate_key(master_password):
    return generate_db_key(master_password)

# Encrypt a password
def encrypt_password(key, password):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

# Decrypt a password
def decrypt_password(key, encrypted_password):
    try:
        cipher_suite = Fernet(key)
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        return decrypted_password
    except InvalidToken:
        return None  # Return None if decryption fails

def initialize_db(key):
    if not os.path.exists(db_path) and not os.path.exists(encrypted_db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                service TEXT NOT NULL,
                encrypted_password BLOB NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        # Encrypt the newly created database
        encrypt_db(db_path, key)

def add_password(service, encrypted_password, key):
    # Decrypt the database before modifying
    decrypt_db(encrypted_db_path, key)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO passwords (service, encrypted_password) VALUES (?, ?)', (service, encrypted_password))
    conn.commit()
    conn.close()
    # Encrypt the database after modification
    encrypt_db(db_path, key)

def retrieve_password(service, key):
    # Decrypt the database before reading
    decrypt_db(encrypted_db_path, key)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT encrypted_password FROM passwords WHERE service = ?', (service,))
    result = c.fetchone()
    conn.close()
    # Re-encrypt the database after reading
    encrypt_db(db_path, key)
    return result[0] if result else None


def main():
    master_password = getpass('Enter your master password: ')
    key = generate_key(master_password)

    # Decrypt the database at startup if needed
    if os.path.exists(encrypted_db_path):
        decrypt_db(encrypted_db_path, key)
    initialize_db(key)  # Pass key to initialize_db

    while True:
        print("\nPassword Manager")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            service = input("Enter the service name: ")
            password = getpass("Enter the password to store: ")
            encrypted_password = encrypt_password(key, password)
            add_password(service, encrypted_password, key)  # Pass key to add_password
            print(f"Password for {service} added successfully.")
        
        elif choice == '2':
            service = input("Enter the service name: ")
            encrypted_password = retrieve_password(service, key)  # Pass key to retrieve_password
            if encrypted_password:
                password = decrypt_password(key, encrypted_password)
                if password:
                    print(f"Password for {service}: {password}")
                else:
                    print("Failed to decrypt the password. Please check your master password.")
            else:
                print(f"No password found for {service}.")

        elif choice == '3':
            print("Exiting password manager.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
