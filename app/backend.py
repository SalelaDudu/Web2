from . import app, database as db, decryptar, encryptar,app_bcrypt
from app.config import SECRET_KEY

def logar(username,password):
    senhaBanco = db.consulta(f'SELECT password FROM login WHERE username = "{username}";')
    if len(senhaBanco) == 0:
        return 1
    else:
        if(decryptar(senhaBanco[0][0],password)):
            user_type = db.consulta(f'SELECT user_mode from user_data WHERE login_username = "{username}"')
            return [2,user_type[0][0]]

def registro(username,senha,re_senha,user_mode):
    consultado = db.consulta(f'''select username from login where username = "{username}";''')
    if(len(consultado) > 0):
        return 1
    else:
        if(senha != re_senha):
             return 2
        else:
            pw_hash = encryptar(senha)
            db.registerLogin(username,pw_hash)
            db.registerUser(username,user_mode)
            return 3

def saveDevInfo(login,nome,nascimento,descricao):
    try:    
        db.registerDevData(login,nome,nascimento,descricao)
    
    except NameError:
        return print(NameError)
def getDevInfo(login):
    try:
        devInfo = db.getDevInfo(login)

        if devInfo[0][2] == None:
            nome = ''
        else:
            nome = devInfo[0][2]
        
        if devInfo[0][5] == None:
            desc = ''
        else:
            desc = devInfo[0][5]
        
        info = {'nome':nome,'nascimento':devInfo[0][3],'descricao': desc}
                
        return info
    except NameError:
        return NameError


def saveRecruiterInfo(login,nome_empresa,descricao_empresa):
    try:
        db.registerRecruiterData(login,nome_empresa,descricao_empresa)
    except NameError:
        return NameError
    
def getRecruiterInfo(login):
    try:
        recruiterInfo = db.getRecruiterInfo(login)
        
        if recruiterInfo[0][2] == None:
            nome = ''
        else:
            nome = recruiterInfo[0][2]
        
        if recruiterInfo[0][5] == None:
            desc = ''
        else:
            desc = recruiterInfo[0][5]
        
        info = {'nome':nome,'descricao': desc}
        return info
        
    except NameError:
        return NameError

def postarVaga(login,nome,descricao):
    try:
        db.postVaga(login,nome,descricao)
    except NameError:
        return NameError