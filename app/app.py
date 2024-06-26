from . import app,session,render_template,request,flash,session,redirect,render_template_string
import app.backend as be
from app.config import SECRET_KEY

@app.route("/")
def index():
    cards = be.getCards()
    if 'login' not in session:
        return render_template("index.html",cards_ = cards)
    else:
        
        if session['user_mode'] == 'Dev':
            dev = session['login']
            session['vagasAplicadas'] = be.consulta(f'''select vaga from candidatos where dev = "{dev}"''')
        return render_template("index.html",session_=session, cards_ = cards)
@app.route("/authentication")
def loginScreen():
    return render_template("authentication.html")
@app.route('/LogOut')
def LogOut():
    session.clear()
    return redirect('/')
@app.route("/logar", methods=['POST'])
def logar():
    username = request.form['login_input']
    password = request.form['login_password_input']
    
    res = be.logar(username,password)
    
    if res == 1:
        flash([0,"Usuário não cadastrado! faça seu registro."])
        return redirect("/authentication#register")
    else:
        if res[0] == 2:
            session['login'] = username
            session['user_mode'] = res[1]
            session.permanent = True
            return dashboard()
        else:
            flash([2,"Usuário e/ou senha incorretos."])
            return redirect('/authentication#logIn')
@app.route('/registro', methods=['POST'])
def registro():

    username = request.form['registro_input']
    senha = request.form['registro_password_input']
    re_senha = request.form['password_input_repeat']
    user_mode = request.form['user_mode']
    res = be.registro(username,senha,re_senha,user_mode)

    if(res == 1):
        flash([1,'Nome de usuário já cadastrado'])
        return redirect('/authentication#register')
    else:
        if(res == 2):
            flash([2,'As senhas não batem!'])
            return redirect('/authentication#register')
        elif res == 3:            
            flash([3,'Sucesso!'])
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
    telefone = request.form['telefone']
    email = request.form['email']
    descricao = request.form['descricao_dev']
    try:
        be.saveDevInfo(login,nomeUsuario,telefone,email,descricao)
        flash('Salvo!')
        return redirect('/dashboard')
    except NameError:
        return(NameError)
@app.route('/saveRecruiterInfo',methods=['POST','GET'])
def recruiterInfo():
    nome_empresa = request.form['nome_empresa']
    descricao_empresa = request.form['descricao_empresa']
    try:
        be.saveRecruiterInfo(session['login'],nome_empresa,descricao_empresa)
        flash('Salvo!')
        return redirect('/dashboard')
    except NameError:
        return NameError
@app.route('/postarVaga',methods=['POST','GET'])
def PostarVaga():
    nome  = request.form['nome_empresa']
    descricao = request.form['descricao_vaga']
    
    try:
        be.postarVaga(session['login'],nome,descricao)
        flash("Postado!")
        return redirect('/dashboard')        
        
    except NameError:
        return NameError
    
@app.route('/minhasVagas')
def minhasVagas():
    if 'login' not in session:
        return redirect('/authentication#logIn')
    else:
        vagas = be.getVagas(session['login'])
        return render_template('minhasvagas.html', _session=session['login'],_vagas=vagas)
@app.route('/candidatarse/<idvaga>')
def candidatar(idvaga):
    if 'login' not in session:
        return redirect('/authentication#logIn')
    else:
        user = session['login']
        vaga = idvaga
        try:
            res = be.consulta(f'select * from candidatos where dev ="{user}" and vaga="{vaga}"')        
            if(len(res) > 0):
                flash([0,"Já se candidatou a essa vaga!"])
                return redirect('/')
            else:
                if be.candidatar(user,vaga) == 'ok':
                    flash([1,'Candidatado com sucesso!'])
                    return redirect('/')
        except NameError:
            return NameError
@app.route('/verCandidato/<idvaga>')
def verCandidatos(idvaga):
    res = be.verCandidatos(idvaga)
    vaga = be.consulta(f'select title,description from cards where id = "{idvaga}"')
    return render_template('/candidatos.html',_session=session['login'], candidatos=res,vaga_=vaga[0])