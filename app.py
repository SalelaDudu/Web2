from flask import Flask,render_template,request
from database_manager import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def loginScreen():
    query = '''select * from login;'''
    handler = consulta(query)
    return render_template("login.html",teste=handler)

@app.route('/registro', methods=['POST'])
def registro():

    email = request.form['username']
    senha = request.form['password']