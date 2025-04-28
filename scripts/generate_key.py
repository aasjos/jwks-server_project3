import sqlite3
import time
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import base64

# Padding function for AES encryption (AES.block_size = 16 bytes)
def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

# AES Encryption function (Encrypt data using AES in ECB mode)
def aes_encrypt(data, key):
    key = pad(key)[:32]  # Ensure the key is the right size (32 bytes for AES-256)
    cipher = AES.new(key, AES.MODE_ECB)  # AES encryption in ECB mode
    encrypted = cipher.encrypt(pad(data))  # Encrypt the data after padding it
    return encrypted

# Function to generate RSA private key, encrypt it, and store it in the database
def generate_and_store_key():
    # Step 1: Generate an RSA private key
    rsa_key = RSA.generate(2048)
    private_key_bytes = rsa_key.export_key()  # Export the private key as bytes

    # Step 2: AES encrypt the private key
    NOT_MY_KEY = os.getenv('NOT_MY_KEY', 'default_key').encode()  # Key for AES encryption
    encrypted_private_key = aes_encrypt(private_key_bytes, NOT_MY_KEY)

    # Step 3: Connect to the SQLite database and store the encrypted private key
    conn = sqlite3.connect("totally_not_my_privateKeys.db")  # Open the SQLite database
    cur = conn.cursor()

    # Insert the encrypted private key and its expiration time into the database
    cur.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", 
                (encrypted_private_key, int(time.time()) + 3600))  # Expires in 1 hour

    conn.commit()  # Commit the changes to the database
    conn.close()   # Close the connection

    print(" Encrypted key generated and stored!")  # Confirm success

# Call the function when the script is run directly
if __name__ == "__main__":
    generate_and_store_key()
