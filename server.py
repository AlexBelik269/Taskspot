from flask import Flask, jsonify, request, send_from_directory, session, render_template # type: ignore
from flask_cors import CORS # type: ignore
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app, supports_credentials=True)
database_path = 'databank.db'

def get_db_connection():
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'home.html')


# -------- TASKS --------
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


# -------- MESSAGE --------
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
        session['username'] = user['username']
        session['user_id'] = user['userID']
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

    
# -------- SIGNUP --------
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


# -------- OTHER --------
@app.route('/get-job')
def serve_get_job():
    return send_from_directory(app.static_folder, 'get-job/get-job.html')

#@app.route('/<path:path>')
#def serve_static_files(path):
#    return send_from_directory(app.static_folder, path)

@app.route('/')
def home():
    logged_in = 'username' in session
    return render_template('home.html', logged_in=logged_in)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return jsonify({'success': True})



# -------- USER --------
@app.route('/user')
def get_user():
    if 'userEmail' in session:
        print(f"Session userEmail: {session['userEmail']}")  # Debugging information
        return jsonify(userEmail=session['userEmail'])
    print("Unauthorized access to /user")  # Debugging information
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/user_messages')
def user_messages():
    if 'userEmail' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.messageID, m.text, m.feedback, u.userEmail as sender
        FROM messages m
        JOIN users u ON m.userID = u.userID
        JOIN tasks t ON m.fk_taskID = t.taskID
        WHERE t.taskID IN (
            SELECT taskID FROM tasks WHERE userID = (SELECT userID FROM users WHERE userEmail = ?)
        )
    ''', (session['userEmail'],))
    messages = cursor.fetchall()
    conn.close()
    message_list = [
        {"messageID": message[0], "text": message[1], "feedback": message[2], "sender": message[3]}
    for message in messages]
    return jsonify(messages=message_list)

@app.route('/user_job_posts' )
def user_job_posts():
    if 'userEmail' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.taskID, t.title
        FROM tasks t
        JOIN users u ON t.userID = u.userID
        WHERE u.userEmail = ?
    ''', (session['userEmail'],))
    tasks = cursor.fetchall()
    job_posts = []
    for task in tasks:
        cursor.execute('''
            SELECT m.messageID, m.text, u.userEmail as sender
            FROM messages m
            JOIN users u ON m.userID = u.userID
            WHERE m.fk_taskID = ?
        ''', (task[0],))
        messages = cursor.fetchall()
        job_posts.append({
            "taskID": task[0],
            "title": task[1],
            "messages": [{"messageID": message[0], "text": message[1], "sender": message[2]} for message in messages]
        })
    conn.close()
    return jsonify(jobPosts=job_posts)


# Custom function to list all endpoints
def list_endpoints():
    endpoints = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':  # Exclude static routes
            endpoints.append({
                'url': str(rule),
                'methods': list(rule.methods),
                'endpoint': rule.endpoint
            })
    return endpoints

@app.route('/list_endpoints')
def show_endpoints():
    return jsonify(list_endpoints())


if __name__ == '__main__':
    app.run(debug=True)



