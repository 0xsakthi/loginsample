from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages and sessions

# Configuration for the authentication API
AUTH_API_URL = "http://localhost:5001/api/authenticate"


@app.route('/')
def home():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Make a request to the authentication API
        try:
            response = requests.post(
                AUTH_API_URL,
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                auth_data = response.json()
                if auth_data.get('authenticated'):
                    session['username'] = username
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))
                else:
                    error = auth_data.get('message', 'Invalid credentials. Please try again.')
            else:
                error = f"Authentication service error: {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            error = f"Could not connect to authentication service: {str(e)}"
    
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
