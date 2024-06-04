from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import sqlite3
import hashlib

app = Flask(__name__, static_folder='taskspot')
CORS(app)
database_path = 'databank.db'

def get_db_connection():
    conn = sqlite3.connect('databank.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()

    task_list = []
    for task in tasks:
        task_list.append({
            'taskID': task['taskID'],
            'title': task['title'],
            'city': task['city'],
            'description': task['description'],
            'duration': task['duration'],
            'price': task['price']
        })
    return jsonify(task_list)

@app.route('/save_message', methods=['POST'])
def save_message():
    task_id = request.form['fk_taskID']
    message_text = request.form['text']

    conn = get_db_connection()
    conn.execute('INSERT INTO messages (fk_taskID, text) VALUES (?, ?)',
                 (task_id, message_text))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/save_task', methods=['POST'])
def save_task():
    title = request.form['title']
    description = request.form['description']
    city = request.form['city']
    duration = request.form['duration']
    price = request.form['price']

    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, description, city, duration, price) VALUES (?, ?, ?, ?, ?)',
                 (title, description, city, duration, price))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

def get_db_connection():
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn

# -------- LOGIN --------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = hashlib.sha256(data.get('password').encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

# -------- SIGNUP ----------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = hashlib.sha256(data.get('password').encode()).hexdigest()
    city = data.get('city')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Email already exists'})

    cursor.execute('INSERT INTO users (username, password, email, user_city) VALUES (?, ?, ?, ?)', (username, password, email, city))
    conn.commit()
    conn.close()

    return jsonify({'success': True})



# Serve the HTML file
@app.route('/get-job')
def serve_get_job():
    return send_from_directory(app.static_folder, 'get-job/get-job.html')

# Serve other static files like CSS, JS
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
