from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup function
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    # Insert a test user if not exists
    cursor.execute("SELECT * FROM users WHERE username=?", ('admin',))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      ('admin', 'password123'))  # In production, use hashed passwords
    
    conn.commit()
    conn.close()


@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'authenticated': False, 'message': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    # Connect to the database and check credentials
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return jsonify({'authenticated': True, 'message': 'Authentication successful'})
    else:
        return jsonify({'authenticated': False, 'message': 'Invalid username or password'})


if __name__ == '__main__':
    setup_database()  # Setup and initialize the database
    app.run(debug=True, port=5001)
