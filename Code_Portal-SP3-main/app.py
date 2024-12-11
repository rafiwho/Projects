from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

#sudo /opt/lampp/manager-linux-x64.run

# Database configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'code_portal'
}

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        # Check the credentials against the MySQL database
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE uname = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result and result[0] == password:
                return jsonify({'status': 'success', 'username': username})
            else:
                return jsonify({'status': 'error', 'message': 'Wrong username or password'})

        except mysql.connector.Error as err:
            return jsonify({'status': 'error', 'message': str(err)})

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        
        # Insert the data into the MySQL database
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (uname, email, password) VALUES (%s, %s, %s)", (username, email, password))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'status': 'success', 'message': 'User registered successfully!'})
        except mysql.connector.Error as err:
            return jsonify({'status': 'error', 'message': str(err)})
    
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
