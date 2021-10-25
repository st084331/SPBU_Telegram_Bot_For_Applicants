import sqlite3

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('user_data.db', check_same_thread=False)
    return __connection


def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
    user_id INTEGER NOT NULL,
    langue TEXT,
    foreigner TEXT, 
    deg TEXT
    )
    ''')
    conn.commit()


def add_user(user_id, langue, foreigner, deg):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM user_data WHERE user_id = {user_id} ")
    if c.fetchone() is None:
        c.execute('INSERT INTO user_data (user_id, langue, foreigner, deg) VALUES (?, ?, ?, ?)',
                  (user_id, langue, foreigner, deg))
    conn.commit()


def change_language(user_id, langue, foreigner, deg):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM user_data WHERE user_id = {user_id}")
    if c.fetchone() is None:
        add_user(user_id, langue, foreigner, deg)
    else:
        c.execute(f"UPDATE user_data SET langue = '{langue}' WHERE user_id = {user_id}")
    conn.commit()


def get_language(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT langue FROM user_data WHERE user_id = {user_id}")
    lang = c.fetchone()
    if lang is None:
        conn.commit()
        return "None"
    elif lang == ('ENG',):
        conn.commit()
        return "ENG"
    elif lang == ('RUS',):
        conn.commit()
        return "RUS"
    elif lang == ('None',):
        conn.commit()
        return "None"


def change_foreigner(user_id, langue, foreigner, deg):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM user_data WHERE user_id = {user_id}")
    if c.fetchone() is None:
        add_user(user_id, langue, foreigner, deg)
    else:
        c.execute(f"UPDATE user_data SET foreigner = '{foreigner}' WHERE user_id = {user_id}")
    conn.commit()


def get_foreigner(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT foreigner FROM user_data WHERE user_id = {user_id}")
    lang = c.fetchone()
    if lang is None:
        conn.commit()
        return "None"
    elif lang == ('YES',):
        conn.commit()
        return "YES"
    elif lang  == ('NO',):
        conn.commit()
        return "NO"
    elif lang == ('None',):
        conn.commit()
        return "None"


def change_degree(user_id, langue, foreigner, deg):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM user_data WHERE user_id = {user_id}")
    if c.fetchone() is None:
        add_user(user_id, langue, foreigner, deg)
    else:
        c.execute(f"UPDATE user_data SET deg = '{deg}' WHERE user_id = {user_id}")
    conn.commit()


def get_degree(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT deg FROM user_data WHERE user_id = {user_id}")
    lang = c.fetchone()
    if lang is None:
        conn.commit()
        return "None"
    elif lang == ('Bachelor',):
        conn.commit()
        return "Bachelor"
    elif lang == ('Master',):
        conn.commit()
        return "Master"
    elif lang == ('PhD',):
        conn.commit()
        return "PhD"
    elif lang == ('Residency',):
        conn.commit()
        return "Residency"
    elif lang == ('None',):
        conn.commit()
        return "None"

#init_db()