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

@app.route('/LogOut')
def LogOut():
    session.clear()
    return'''

        <h1>Até logo! Você será redirecionado em <span id="countdown">3</span> segundos...</h1>
        <script>
            function startCountdown(duration, display) {
                var timer = duration, seconds;
                var countdownInterval = setInterval(function() {
                    seconds = parseInt(timer, 10);
                    display.textContent = seconds;

                    if (--timer < 0) {
                        clearInterval(countdownInterval);
                        window.location.href = "/";
                    }
                }, 1000);
            }

            window.onload = function() {
                var threeSeconds = 3;
                var display = document.querySelector('#countdown');
                startCountdown(threeSeconds, display);
            };            
        </script>             
    '''
@app.route("/logar", methods=['POST'])
def logar():
    username = request.form['login_input']
    password = request.form['login_password_input']
    
    res = be.logar(username,password)
    
    if res == 1:
        flash("Usuário não cadastrado! faça seu registro.")
        return redirect("/authentication#register")
    else:
        if res[0] == 2:
            flash("LOGADO!")
            session['login'] = username
            session['user_mode'] = res[1]
            session.permanent = True
            return dashboard()
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

@app.route('/dashboard')
def dashboard():
    if 'login' not in session:
        return redirect('/authentication#logIn')
    else:
        try:
            if session['user_mode'] == 'Dev':
                info = be.getDevInfo(session['login'])
            elif session['user_mode'] == 'Recrutador':
                info = be.getRecruiterInfo(session['login'])
            
            return render_template("dashboard.html",_session = session, _info = info)
        except NameError:
            return NameError
@app.route('/saveDevInfo', methods=['POST','GET'])

def devInfo():
    login = session['login']
    nomeUsuario = request.form['nome_dev']
    nascimento = request.form['nascimento']
    descricao = request.form['descricao_dev']
    try:
        be.saveDevInfo(login,nomeUsuario,nascimento,descricao)
        return redirect('/dashboard')
    except NameError:
        return(NameError)

@app.route('/saveRecruiterInfo',methods=['POST','GET'])
def recruiterInfo():
    nome_empresa = request.form['nome_empresa']
    descricao_empresa = request.form['descricao_empresa']
    try:
        be.saveRecruiterInfo(session['login'],nome_empresa,descricao_empresa)
        return redirect('/dashboard')
    except NameError:
        return NameError