from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='taskspot')
CORS(app)

def connect_to_database():
    return sqlite3.connect('databank.db')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT title, description, city, duration, price FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    task_list = []
    for task in tasks:
        task_dict = {
            "title": task[0],
            "description": task[1],
            "place": task[2],
            "duration": task[3],
            "price": task[4]
        }
        task_list.append(task_dict)

    return jsonify(task_list)

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
