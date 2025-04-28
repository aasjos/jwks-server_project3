from Crypto.Cipher import AES
import os

def pad(data):
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def aes_encrypt(data, key):
    key = key.ljust(32, b'\0')[:32]  # Make key exactly 32 bytes (AES-256)
    iv = os.urandom(16)  # Random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data))
    return iv + encrypted  # Store IV + ciphertext

def aes_decrypt(encrypted_data, key):
    key = key.ljust(32, b'\0')[:32]  # Make key exactly 32 bytes (AES-256)
    iv = encrypted_data[:16]  # First 16 bytes are IV
    encrypted = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    return unpad(decrypted)
