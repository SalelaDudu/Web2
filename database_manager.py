from sqlite3 import *
from flask import g

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect('./database/app.db')
    return db

def consulta(query):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()