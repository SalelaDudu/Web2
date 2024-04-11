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
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()

    return render_template('register.html')
    
    '''
    try:
        username = request.form['username']
        password = request.form['password']

        return username,password
        
    except(ValueError,ValueError) as e:
        return e
        