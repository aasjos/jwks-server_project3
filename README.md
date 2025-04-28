 JWKS Server - Project 3
This is a simple JWKS (JSON Web Key Set) server implemented using Flask.
It includes user registration, authentication, encrypted private key storage, and JWT issuance.

Features
User registration with auto-generated secure passwords.

Passwords are securely hashed using Argon2.

Private RSA keys are AES-encrypted and stored in SQLite database.

JWT tokens are generated using decrypted private keys.

Auth requests are logged with IP addresses.

Rate-limiting applied to the /auth endpoint (optional).

Setup Instructions
Install Requirements

bash
 
 
pip install -r requirements.txt
Set environment variable

bash
 
 
export NOT_MY_KEY="this_is_a_very_secure_key123!"
Run the Server

bash
 
bash run.sh
The server will be running at:

cpp
 
http://127.0.0.1:5000
Endpoints
POST /register

Registers a new user.

Body:

json
Copy
Edit
{
    "username": "your_username",
    "email": "your_email@example.com"
}
Response: Returns an auto-generated password.

POST /auth

Authenticates the user and returns a JWT token.

Body:

json
Copy
Edit
{
    "username": "your_username",
    "password": "your_generated_password"
}
GET /.well-known/jwks.json

Returns public keys for JWT verification.

Database Tables
users - Stores user credentials (username, hashed password, email, etc.)

auth_logs - Logs authentication attempts.

keys - Stores encrypted private RSA keys with expiry timestamps.

 
 
