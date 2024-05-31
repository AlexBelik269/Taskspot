import sqlite3

def connect_to_database():
    return sqlite3.connect('databank.db')

def display_table_data():
    conn = connect_to_database()
    cursor = conn.cursor()

    print("\nUsers Table:")
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)

    print("\nTasks Table:")
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        print(task)

    print("\nMessages Table:")
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    for message in messages:
        print(message)

    conn.close()

if __name__ == '__main__':
    display_table_data()
