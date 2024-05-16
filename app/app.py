from . import app,session,render_template,request,flash,session,redirect,render_template_string
import app.backend as be
from app.config import SECRET_KEY

@app.route("/")
def index():
    if 'login' not in session:
        return render_template("index.html")
    else:                
        return render_template("index.html",session_ = session['login'])

@app.route("/authentication")
def loginScreen():
    return render_template("authentication.html")

@app.route('/closeSession')
def closeSession():
    session.clear()
    return '<h1>Session close!</h1>'

@app.route("/logar", methods=['POST'])
def logar():
    username = request.form['login_input']
    password = request.form['login_password_input']
    
    res = be.logar(username,password)
    
    if res == 1:
        flash("Usuário não cadastrado! faça seu registro.")
        return redirect("/authentication#register")
    else:
        if res == 2:
            flash("LOGADO!")
            session['login'] = username
            session.permanent = True
            return redirect('/')
        else:
            flash("Usuário e/ou senha incorretos.")
            return redirect('/authentication#logIn')
        
@app.route('/registro', methods=['POST'])
def registro():

    username = request.form['registro_input']
    senha = request.form['registro_password_input']
    re_senha = request.form['password_input_repeat']
    user_mode = request.form['user_mode']
    res = be.registro(username,senha,re_senha,user_mode)

    if(res == 1):
        flash('Nome de usuário já cadastrado')
        return redirect('/authentication#register')
    else:
        if(res == 2):
            flash('As senhas não batem!')
            return redirect('/authentication#register')
        elif res == 3:            
            flash('Sucesso!')
            return redirect('/authentication#logIn')