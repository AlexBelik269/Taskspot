import sqlite3
import hashlib

def connect_to_database():
    return sqlite3.connect('databank.db')

database_path = 'databank.db'

conn = sqlite3.connect(database_path)
cursor = conn.cursor()


def initialize_database():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS users;')
    cursor.execute('DROP TABLE IF EXISTS tasks;')
    cursor.execute('DROP TABLE IF EXISTS messages;')

    cursor.execute('''CREATE TABLE users
                  (userID INTEGER PRIMARY KEY, 
                   username TEXT, 
                   password TEXT,
                   email TEXT,
                   user_city TEXT)
               ''')

    cursor.execute('''CREATE TABLE tasks 
                  (taskID INTEGER PRIMARY KEY,
                   title TEXT ,
                   description TEXT, 
                   city TEXT, 
                   duration TEXT, 
                   price INTEGER)
               ''')
    
    cursor.execute('''CREATE TABLE messages 
                  (messageID INTEGER PRIMARY KEY AUTOINCREMENT,
                   text TEXT,
                   fk_taskID INTEGER,
                   userID INTEGER,
                   feedback TEXT,
                   FOREIGN KEY (fk_taskID) REFERENCES tasks(taskID),
                   FOREIGN KEY (userID) REFERENCES users(userID))
               ''')

    Users = [
        ('MaliDoli', hashlib.sha256('1234'.encode()).hexdigest(), 'mali@doli.com', 'Basel'),
        ('RichiDom', hashlib.sha256('5678'.encode()).hexdigest(), 'richi@dom.com', 'Luzern'),
        ('TomiMan', hashlib.sha256('789'.encode()).hexdigest(), 'tomi@man.com', 'Chur'),
        ('AniMoni', hashlib.sha256('7777'.encode()).hexdigest(), 'ani@moni.com', 'Sursee'),
        ('RusMus', hashlib.sha256('9876'.encode()).hexdigest(), 'rus@mus.com', 'Geneva'),
        ('User1', hashlib.sha256('123'.encode()).hexdigest(), 'user@1.com', 'Zürich'),
        ('User2', hashlib.sha256('234'.encode()).hexdigest(), 'user@2.com', 'Luzern'),
    ]
    cursor.executemany("INSERT INTO users (username, password, email, user_city) VALUES (?, ?, ?, ?)", Users)


    Tasks = [
        ('Mow the Lawn', 'I need someone to mow my lawn. It\'s a medium-sized garden. Equipment will be provided.', 'Luzern', '2h', '100CHF'),
        ('Grocery Shopping Assistance for Elderly', 'Looking for someone to assist an elderly woman with her grocery shopping. She may need help navigating the store and carrying items.', 'Basel', '3h', '200CHF'),
        ('Dog Walking', 'Need someone to walk my dog. Must be comfortable handling a medium-sized dog.', 'Zürich', '30min', '20CHF'),
        ('House Cleaning', 'Deep cleaning required for a large house. Attention to detail is important. Cleaning supplies will be provided.', 'Luzern', '9h', '1,000CHF'),
        ('Babysitting', 'Looking for a responsible individual to babysit a toddler. Experience with young children preferred.', 'Sursee', '7h', '500CHF'),
        ('Tutoring', 'Seeking a tutor to help with math homework for a high school student. ', 'Zürich', '45min', '30CHF'),
        ('Gardening Assistance', 'Assist with gardening tasks. This includes weeding, planting, and general garden maintenance.', 'Chur', '3h', '130CHF'),
        ('Driving Assistance', 'Need someone to drive with me to improve my driving.', 'Basel', '45min', '30CHF'),
        ('Tech Support', 'Help needed with setting up a new computer.', 'Sursee', '35min', '30CHF'),
        ('House Painting', 'Painting job available. Must have experience with interior painting.', 'Chur', '5h', '300CHF'),
        ('Language Tutoring', 'Looking for a language tutor to practice conversational skills.', 'Zürich', '45min', '80CHF'),
        ('Guitar Lessons', 'Searching for guitar lessons for beginners. Lessons will cover basic chords, strumming techniques, and simple songs.', 'Luzern', '1h', '60CHF'),
        ('Home Organizing', 'Need help organizing closets and decluttering rooms. Must be efficient and have an eye for detail.', 'Basel', '4h', '180CHF'),
        ('Event Photography', 'Hiring a photographer for a birthday party. Must have experience with event photography and provide own equipment.', 'Zürich', '3h', '250CHF'),
        ('Personal Fitness Training', 'Seeking a personal trainer to create a customized workout plan and provide fitness training sessions.', 'Luzern', '1h', '80CHF'),
        ('Car Wash and Detailing', 'Looking for someone to wash and detail my car. Must have experience with car detailing.', 'Sursee', '2h', '70CHF'),
        ('Data Entry Assistance', 'Need help with data entry tasks for a small business. Basic computer skills required.', 'Chur', '3h', '90CHF'),
        ('Landscaping', 'In need for landscaping. Tasks include planting flowers, trimming hedges, and general yard maintenance.', 'Basel', '6h', '300CHF'),
        ('Pet Sitting', 'Looking for a pet sitter to care for two cats and a dog while I\'m away for the weekend. Must be comfortable with pets and able to provide food and water.', 'Zürich', '2d', '150CHF'),
        ('Graphic Design Services', 'Seeking a graphic designer to create a logo for a new business venture. Must provide portfolio for review.', 'Sursee', '4h', '200CHF'),
        ('Home Renovation Assistance', 'Assist with home renovation tasks such as painting, flooring, and carpentry. Experience with home improvement projects preferred.', 'Chur', '8h', '400CHF')
        
        ]

    cursor.executemany("INSERT INTO tasks (title, description, city, duration, price)VALUES (?, ?, ?, ?,?)", Tasks)

    conn.commit()
    conn.close()

#initialize_database()

