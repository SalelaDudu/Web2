from flask import Flask ,flash, redirect, render_template,render_template_string,request,session, url_for
from flask_bcrypt import Bcrypt, bcrypt
from app.database import *
from app.config import SECRET_KEY
import datetime

app = Flask(__name__)
app_bcrypt = Bcrypt(app)

app.secret_key = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=15)

def encryptar(senha):
    return app_bcrypt.generate_password_hash(senha).decode('utf-8')

def decryptar(senhaBanco,senhaCandidata):
    return app_bcrypt.check_password_hash(senhaBanco, senhaCandidata) # returns True
