from encryption import aes_encrypt
import os
import time
from db import get_db_connection
from Crypto.PublicKey import RSA

def generate_and_store_key():
    key = RSA.generate(2048)
    private_key = key.exportKey()
    NOT_MY_KEY = os.getenv('NOT_MY_KEY', '12345678901234567890123456789012').encode()
    encrypted_key = aes_encrypt(private_key, NOT_MY_KEY)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", 
                (encrypted_key, int(time.time()) + 3600))
    conn.commit()
    conn.close()
