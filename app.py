import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask, request, jsonify
from jwks_server.db import get_db_connection
from encryption import aes_encrypt, aes_decrypt
from key_utils import generate_and_store_key
import jwt, time, os
from passlib.hash import argon2
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask app
app = Flask(__name__)


# Setup rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["10 per second"]
)

NOT_MY_KEY = os.getenv('NOT_MY_KEY', 'default_key').encode()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = str(uuid.uuid4())  # Generate a random password using UUIDv4
    hashed_password = argon2.hash(password)  # Hash the password using Argon2

    # Save user in the database
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)", 
                    (username, hashed_password, email))
        conn.commit()
        return jsonify({"password": password}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/auth', methods=['POST'])
@limiter.limit("10 per second")
def auth():
    username = request.json.get('username')
    password = request.json.get('password')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "Invalid user"}), 401

    user_id, password_hash = row

    if not argon2.verify(password, password_hash):
        conn.close()
        return jsonify({"error": "Invalid password"}), 401

    # ✅ Password is correct. NOW log the auth request
    ip = request.remote_addr
    cur.execute("INSERT INTO auth_logs (request_ip, user_id) VALUES (?, ?)", (ip, user_id))
    conn.commit()

    # ✅ Fetch latest encrypted private key
    cur.execute("SELECT kid, key FROM keys ORDER BY exp DESC LIMIT 1")
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "No keys found"}), 500

    kid, encrypted_key = row
    decrypted_key = aes_decrypt(encrypted_key, NOT_MY_KEY)

    private_key = jwt.algorithms.RSAAlgorithm.from_jwk(decrypted_key.decode())

    payload = {
        "sub": username,
        "iat": int(time.time()),
        "exp": int(time.time()) + 600
    }

    token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": str(kid)})

    conn.close()
    return jsonify({"token": token})





@app.route('/.well-known/jwks.json')
def jwks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT kid, key FROM keys")
    keys = []
    for kid, encrypted_key in cur.fetchall():
        decrypted_key = aes_decrypt(encrypted_key, NOT_MY_KEY)
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(decrypted_key.decode()).public_key()
        public_numbers = public_key.public_numbers()
        n = public_numbers.n.to_bytes(256, 'big')
        e = public_numbers.e.to_bytes(3, 'big')
        keys.append({
            "kty": "RSA",
            "use": "sig",
            "kid": str(kid),
            "alg": "RS256",
            "n": jwt.utils.base64url_encode(n).decode(),
            "e": jwt.utils.base64url_encode(e).decode()
        })
    conn.close()
    return jsonify({"keys": keys})

if __name__ == "__main__":
    generate_and_store_key()
    app.run(debug=True)
