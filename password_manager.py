import argparse
import os
import json
from getpass import getpass
from encryption import encrypt, decrypt
from storage import load_data, save_data
from config import KEY_FILE

def get_master_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = os.urandom(32)
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def add_password(service, username, password, master_key):
    """Encrypt and store a password."""
    data = load_data()
    encrypted_password = encrypt(password, master_key)
    data[service] = {"username": username, "password": encrypted_password}
    save_data(data)
    print(f"Stored credentials for {service}.")

def retrieve_password(service, master_key):
    """Retrieve and decrypt a password."""
    data = load_data()
    if service in data:
        username = data[service]["username"]
        decrypted_password = decrypt(data[service]["password"], master_key)
        print(f"Username: {username}\nPassword: {decrypted_password}")
    else:
        print("No credentials found for this service.")

def delete_password(service):
    """Delete stored credentials."""
    data = load_data()
    if service in data:
        del data[service]
        save_data(data)
        print(f"Deleted credentials for {service}.")
    else:
        print("Service not found.")

def main():
    parser = argparse.ArgumentParser(description="Password Manager CLI")
    parser.add_argument("action", choices=["add", "get", "delete"], help="Action to perform")
    parser.add_argument("service", help="Service name")
    parser.add_argument("--username", help="Username (for adding passwords)")
    
    args = parser.parse_args()
    master_key = get_master_key()
    
    if args.action == "add":
        if not args.username:
            print("Username is required to add a password.")
            return
        password = getpass("Enter password: ")
        add_password(args.service, args.username, password, master_key)
    elif args.action == "get":
        retrieve_password(args.service, master_key)
    elif args.action == "delete":
        delete_password(args.service)

if __name__ == "__main__":
    main()

