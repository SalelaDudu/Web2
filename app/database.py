from sqlite3 import *
from flask import g

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect('./app/database/app.db')
    return db

def consulta(query):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def registerLogin(username,psswd):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"insert into login values('{username}','{psswd}');")
    db.commit()
    cursor.close()

def registerUser(login,user_mode):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"insert into user_data(login_username, user_mode) values('{login}','{user_mode}')")
    db.commit()
    cursor.close()