<img width="651" alt="Screenshot 2025-04-27 at 11 16 05 PM" src="https://github.com/user-attachments/assets/8aeb844e-290a-4f8b-980c-9ac484158950" />
<img width="854" alt="Screenshot 2025-04-27 at 10 40 28 PM" src="https://github.com/user-attachments/assets/90b05210-7974-466c-9285-dbb3e695bc85" />
<img width="974" alt="Screenshot 2025-04-27 at 10 28 34 PM" src="https://github.com/user-attachments/assets/b6160a1b-c628-4bb5-aa31-72e2904ee7a9" />
<img width="932" alt="Screenshot 2025-04-27 at 10 16 43 PM" src="https://github.com/user-attachments/assets/23263ad6-5b95-4f1e-886e-21168a0b2587" />
<img width="1082" alt="Screenshot 2025-04-27 at 9 10 26 PM" src="https://github.com/user-attachments/assets/c3966c8f-fd0b-4427-b2a6-35a4bad68046" />
JWKS Server - Project 3
This project implements a secure JSON Web Key Set (JWKS) server using Flask, SQLite, and cryptographic techniques. It provides functionalities for secure user registration, authentication, JWT token generation, and JWKS key serving.

- Features
User Registration (/register):

New users can register with a username and email.

A random password is securely generated (UUID) and hashed using Argon2 before storing in the database.
Unique usernames are enforced.

Authentication (/auth):

Users can authenticate with their username and password.

Password verification is handled using Argon2.

On successful login, a JWT token is issued, signed with an encrypted private key.

Login attempts are logged (IP address, timestamp) in an auth_logs table.

JWKS Endpoint (/.well-known/jwks.json):

Publishes the public keys in JWKS format.

Only decrypted public portions of keys are shared, following security best practices.

Private Key Encryption:

Private keys are encrypted using AES (CBC mode) before storing in the database.

A secure environment variable NOT_MY_KEY is used for encryption and decryption.

Security Enhancements:

Rate limiting on /auth endpoint (10 requests per second).

Secure password hashing (Argon2).

Secure key encryption (AES).

Random password generation during registration.

IP Logging during authentication.

- Technologies Used
Python 3.13

Flask

Flask-Limiter

PyCryptodome (for AES encryption)

Passlib (for Argon2 hashing)

SQLite (database)

JWT (PyJWT) (for token signing and verification)

-Database Schema
users table:

id, username, password_hash, email, date_registered, last_login

auth_logs table:

id, request_ip, user_id, timestamp

keys table:

kid, key, exp

- Setup Instructions
Clone the Repository:

 
git clone https://github.com/aasjos/jwks-server_project3.git
cd jwks-server_project3
Install Requirements:

 
pip install -r requirements.txt
Set Environment Variable:

 
export NOT_MY_KEY="your_super_secret_key_32bytes!"
Initialize Database and Keys:

 
 
python3 scripts/init_db.py
python3 scripts/generate_key.py
Run the Flask Server:

 
 
bash run.sh
Test Endpoints using curl or Postman:

/register

/auth

/.well-known/jwks.json

Notes
Ensure your NOT_MY_KEY is exactly 16, 24, or 32 bytes for AES encryption.

This project is for educational purposes and should not be used in production without additional security hardening.

Always run Flask in production behind a WSGI server like Gunicorn.


 
 
 
