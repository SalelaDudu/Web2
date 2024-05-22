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