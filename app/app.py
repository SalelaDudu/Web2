from flask import Flask, flash, redirect, render_template,render_template_string,request,session, url_for
import datetime
from flask_bcrypt import Bcrypt
from database import *

app = Flask(__name__)
app_bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'salamandra'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=10)

def encryptar(senha):
    return app_bcrypt.generate_password_hash(senha).decode('utf-8')

def decryptar(senhaBanco,senhaCandidata):
    return app_bcrypt.check_password_hash(senhaBanco, senhaCandidata) # returns True

from app import app


@app.route("/")
def index():
    print(session)
    if(session['login'] != None):
        session_ =  session['login']
    else:
        session_ = None
                
    return render_template("index.html",session_)

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
            session['login'] = username
            session.permanent = True
            return render_template_string(
            """
            {%if session['login'] %}
                <h1>Welcome {{session['login']}}!</h1>
            {%else%}
                <h1> Welcome! please authenticate <a href="{{url_for('registro')}}"> here</a></h1>
            {%endif%}
            """)
        else:
            flash("Usuário e/ou senha incorretos.")
            return redirect('/authentication#logIn')
        
@app.route('/registro', methods=['POST'])
def registro():

    username = request.form['registro_input']
    senha = request.form['registro_password_input']
    re_senha = request.form['password_input_repeat']
    user_mode = request.form['user_mode']
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
            registerUser(username,user_mode)
            flash('Sucesso!')
            return redirect('/authentication#logIn')

@app.route('/closeSession')
def closeSession():
    
    session.pop('login', default=None)
    return '<h1>Session close!</h1>'