from flask import Flask, jsonify, send_from_directory, request, render_template, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import hashlib

app = Flask(__name__, static_folder='taskspot')
CORS(app)
app.secret_key = 'your_secret_key'  # Ensure this is a secret value
database_path = 'databank.db'

def get_db_connection():
    conn = sqlite3.connect(database_path)
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
    data = request.json
    task_id = data['fk_taskID']
    message_text = data['text']

    conn = get_db_connection()
    conn.execute('INSERT INTO messages (fk_taskID, text) VALUES (?, ?)',
                 (task_id, message_text))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/save_task', methods=['POST'])
def save_task():
    data = request.json
    title = data['title']
    description = data['description']
    city = data['city']
    duration = data['duration']
    price = data['price']

    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, description, city, duration, price) VALUES (?, ?, ?, ?, ?)',
                 (title, description, city, duration, price))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

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
        session['username'] = user['username']
        session['user_id'] = user['userID']
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

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

    cursor.execute('INSERT INTO users (username, password, email, user_city) VALUES (?, ?, ?, ?)', 
                   (username, password, email, city))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/get-job')
def serve_get_job():
    return send_from_directory(app.static_folder, 'get-job/get-job.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/')
def home():
    logged_in = 'username' in session
    return render_template('home.html', logged_in=logged_in)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return jsonify({'success': True})




@app.route('/user', methods=['GET'])
def get_user_data():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    username = session['username']
    return jsonify({'username': username})


@app.route('/user_messages', methods=['GET'])
def get_user_messages():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    username = session['username']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''SELECT m.messageID, m.text, t.title, u.username AS sender, m.fk_taskID
                      FROM messages m
                      JOIN tasks t ON m.fk_taskID = t.taskID
                      JOIN users u ON t.userID = u.userID
                      WHERE u.username = ?''', (username,))
    messages = cursor.fetchall()
    conn.close()

    message_list = []
    for message in messages:
        message_list.append({
            'messageID': message['messageID'],
            'text': message['text'],
            'taskTitle': message['title'],
            'sender': message['sender'],
            'feedback': None  # Placeholder for feedback status
        })

    return jsonify({"messages": message_list})

@app.route('/user_job_posts', methods=['GET'])
def get_user_job_posts():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    username = session['username']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''SELECT t.taskID, t.title, t.description
                      FROM tasks t
                      JOIN users u ON t.userID = u.userID
                      WHERE u.username = ?''', (username,))
    job_posts = cursor.fetchall()

    job_post_list = []
    for job_post in job_posts:
        cursor.execute('''SELECT m.messageID, m.text, u.username AS sender
                          FROM messages m
                          JOIN users u ON m.userID = u.userID
                          WHERE m.fk_taskID = ?''', (job_post['taskID'],))
        messages = cursor.fetchall()

        message_list = []
        for message in messages:
            message_list.append({
                'messageID': message['messageID'],
                'text': message['text'],
                'sender': message['sender']
            })

        job_post_list.append({
            'taskID': job_post['taskID'],
            'title': job_post['title'],
            'description': job_post['description'],
            'messages': message_list
        })

    conn.close()

    return jsonify({"jobPosts": job_post_list})

@app.route('/feedback', methods=['POST'])
def provide_feedback():
    data = request.json
    messageID = data['messageID']
    feedback = data['feedback']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE messages
                      SET feedback = ?
                      WHERE messageID = ?''', (feedback, messageID))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
