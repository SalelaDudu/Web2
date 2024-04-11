from sqlite3 import *
from flask import Flask,render_template,g

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect('./database/app.db')
    return db


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def loginScreen():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''select * from login;''')
    return cursor.fetchall()

