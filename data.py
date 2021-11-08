# This Python file uses the following encoding: utf-8
#!spbubotenv3.9/bin python3
import sqlite3
import config
__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect(f"{config.prefix}user_data.db", check_same_thread=False)
    return __connection


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
    user_id INTEGER NOT NULL,
    language TEXT,
    foreigner TEXT, 
    degree TEXT
    )
    ''')
    conn.commit()


def add_user(user_id, language, foreigner, degree):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM user_data WHERE user_id = {user_id}")
    if c.fetchone() is None:
        c.execute('INSERT INTO user_data (user_id, language, foreigner, degree) VALUES (?, ?, ?, ?)',
                  (user_id, language, foreigner, degree))
    conn.commit()


def change_language(user_id, language, foreigner, degree):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM user_data WHERE user_id = {user_id}")
    if c.fetchone() is None:
        add_user(user_id, language, foreigner, degree)
    else:
        c.execute(f"UPDATE user_data SET language = '{language}' WHERE user_id = {user_id}")
    conn.commit()


def get_language(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT language FROM user_data WHERE user_id = {user_id}")
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


def change_foreigner(user_id, language, foreigner, degree):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM user_data WHERE user_id = {user_id}")
    if c.fetchone() is None:
        add_user(user_id, language, foreigner, degree)
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


def change_degree(user_id, language, foreigner, degree):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM user_data WHERE user_id = {user_id}")
    if c.fetchone() is None:
        add_user(user_id, language, foreigner, degree)
    else:
        c.execute(f"UPDATE user_data SET degree = '{degree}' WHERE user_id = {user_id}")
    conn.commit()


def get_degree(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT degree FROM user_data WHERE user_id = {user_id}")
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