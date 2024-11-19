# Standard library imports
import os
import secrets
import string
from urllib.parse import urlparse

# Third-party imports
import psycopg2
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

def get_db_connection():
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:pgpassword@db:5432/postgres")
    parsed_db_url = urlparse(db_url)
    
    return psycopg2.connect(
        # Extract connection parameters from the parsed DB URL
        dbname=parsed_db_url.path[1:],  # Skip leading '/'
        user=parsed_db_url.username,
        password=parsed_db_url.password,
        host=parsed_db_url.hostname,
        port=parsed_db_url.port
    )

def generate_secret_path(path_length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(path_length))

def encrypt(fkey, token):
    f = Fernet(fkey)
    return f.encrypt(token.encode())

def decrypt(fkey, token):
    f = Fernet(fkey)
    return f.decrypt(token.decode())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    plaintext_message = request.form['text']
    secret_path = generate_secret_path()

    if plaintext_message == "":
        return "Oops! Cannot process an empty message. Return to the home page and try again."

    # Encrypt the secret so that it isn't stored in plaintext
    fkey = Fernet.generate_key()
    encrypted_value = encrypt(fkey, plaintext_message)

    # Use context managers to ensure the connection and cursor are properly managed
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Ensure the table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS secrets_schema.secrets_table (
                    id SERIAL PRIMARY KEY,
                    fkey BYTEA UNIQUE NOT NULL,
                    value BYTEA UNIQUE NOT NULL,
                    path VARCHAR(255) UNIQUE NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            
            # Insert the new secret
            cursor.execute("""
                INSERT INTO secrets_schema.secrets_table (fkey, value, path, is_active)
                VALUES (%s, %s, %s, %s)
            """, (fkey, encrypted_value, secret_path, True))
            
            # Save changes made during a transaction to the DB
            conn.commit()

    return request.host_url + "get/" + secret_path

@app.route('/get/<secret_path>', methods=['GET'])
def retrieve(secret_path):
    # Use context managers to ensure the connection and cursor are properly managed
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Select the matching rows
            cursor.execute("""
                SELECT fkey, value FROM secrets_schema.secrets_table
                WHERE path = %s AND is_active = %s
            """, (secret_path, True))

            # Select the first entry (there should only be one match)
            row = cursor.fetchone()

            if row:  # Exists
                # From the SELECT query, we extracted the Fernet key and encrypted value
                fkey, value = row

                # Ensure fkey and value are in bytes format
                if isinstance(fkey, memoryview):
                    fkey = fkey.tobytes()
                if isinstance(value, memoryview):
                    value = value.tobytes()
                
                # Ready to decrypt
                result = decrypt(fkey, value)

                # Delete the row from the DB since we only want to access the secret once anyways
                cursor.execute("""
                    DELETE FROM secrets_schema.secrets_table WHERE path = %s
                """, (secret_path,))
                
                # Save changes made during a transaction to the DB
                conn.commit()
            else:  # Does not exist
                result = "Oops! Either the secret expired or the URL is wrong. Return to the home page and try again."

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
