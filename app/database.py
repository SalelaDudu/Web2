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
    
def registerDevData(login,name,birth,desc):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"update user_data set name='{name}',born='{birth}',description='{desc}' where login_username = '{login}'")
    db.commit()
    cursor.close()

def registerRecruiterData(login,name,desc):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"update user_data set name='{name}',description='{desc}' where login_username = '{login}'")
    db.commit()
    cursor.close()

def getDevInfo(login):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"select * from user_data where login_username = '{login}'")
    return cursor.fetchall()

def getRecruiterInfo(login):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"select * from user_data where login_username = '{login}'")
    return cursor.fetchall()

def postVaga(login,nome,descricao):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"insert into cards('owner','description','title') values('{login}','{descricao}','{nome}')")
    db.commit()
    cursor.close()

def getCards():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"select * from cards")
    return cursor.fetchall()

def getMyVagas(owner):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"select title,description from cards where owner = '{owner}'")
    return cursor.fetchall()
    