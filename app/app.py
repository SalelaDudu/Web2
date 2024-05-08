from flask import Flask, flash, redirect, render_template,request, url_for
from flask_bcrypt import Bcrypt
from database import *

app = Flask(__name__)
app_bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'salamandra'

def encryptar(senha):
    return app_bcrypt.generate_password_hash(senha).decode('utf-8')

def decryptar(senhaBanco,senhaCandidata):
    return app_bcrypt.check_password_hash(senhaBanco, senhaCandidata) # returns True

from app import app


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/authentication")
def loginScreen():
    return render_template("authentication.html")
    

@app.route("/logar", methods=['POST'])
def logar():
    username = request.form['login_input']
    password = request.form['login_password_input']
    senhaBanco = consulta(f'select password from login where username = "{username}"')
    if(len(senhaBanco) == 0):
        flash("Usuário não cadastrado! faça seu registro.")
        return redirect("/authentication#register")
    else:
        if(decryptar(senhaBanco[0][0],password)):
            flash("LOGADO!")
            return redirect('/authentication#logIn')
        else:
            flash("Usuário e/ou senha incorretos.")
            return redirect('/authentication#logIn')
        
@app.route('/registro', methods=['POST'])
def registro():

    username = request.form['registro_input']
    senha = request.form['registro_password_input']
    re_senha = request.form['password_input_repeat']
    consultado = consulta(f'''select username from login where username = "{username}";''')

    if(len(consultado) > 0):
        flash('Nome de usuário já cadastrado')
        return redirect('/authentication#register')
    else:
        if(senha != re_senha):
            flash('As senhas não batem!')
            return redirect('/authentication#register')
        else:
            pw_hash = encryptar(senha)
            registerLogin(username,pw_hash)
            return redirect('/authentication#logIn')