from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mercado.db"
db.init_app(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(length = 30), nullable = False, unique = True)
    preco = db.Column(db.Integer, nullable = False)
    cod_barra = db.Column(db.String(length = 12),nullable = False, unique = True)
    cod_barra = db.Column(db.String(length = 1024),nullable = False, unique = True)


@app.route('/')
def page_home():
    return render_template("index.html")

@app.route('/produtos')
def page_produto():
    itens = [{'id':1,'nome':"Celular",'cod_barra':"23721831",'preco':1200},
             {'id':2,'nome':"Notebook",'cod_barra':"5283463",'preco':3500},
             {'id':3,'nome':"Teclado",'cod_barra':"23762178",'preco':120},
             {'id':4,'nome':"Monitor",'cod_barra':"127321838",'preco':800},
             {'id':5,'nome':"Mouse",'cod_barra':"3223123",'preco':221}]
    return render_template("produtos.html",itens=itens)
    