from flask import Flask, render_template, request, redirect, url_for
from utils import db, lm
import os
from flask_migrate import Migrate
from models import *
from controllers.diario import bp_diario
from controllers.usuario import bp_usuario
from controllers.capitais import bp_capitais

app = Flask(__name__)
app.register_blueprint(bp_diario, url_prefix='/diario') #url prefix
app.register_blueprint(bp_usuario, url_prefix='/usuario')
app.register_blueprint(bp_capitais, url_prefix='/capitais')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
mydb = os.getenv('DB_DATABASE')

conexao = f"mysql+pymysql://{username}:{password}@{host}/{mydb}"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao


db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)

@app.errorhandler(401)
def acesso_negado(e):
    return render_template('acesso_negado.html')

@app.errorhandler(404)
def acesso_negado(e):
    return render_template('not_found.html')


@app.route('/')
def index():
    return render_template('index.html')

#------ ROTAS DO ARQUIVO da base.html --------

@app.route("/pagina_inicial")
def pagina_inicial():
    return render_template('pagina_inicial.html')

@app.route("/cadastrar_capitais")
def cadastrar_capitais():
    return render_template('cadastrar_capitais.html')

@app.route("/fala_conosco")
def fale_conosco():
    return render_template('fale_conosco.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/buscar")
def buscar():
    return render_template('buscar.html')

if __name__ == '__main__':
    app.run(debug=True)

