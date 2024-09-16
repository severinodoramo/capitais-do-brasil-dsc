from flask import render_template, request, redirect, flash, url_for
from utils import db, lm
from models.usuario import Usuario
from flask import Blueprint
from flask_login import login_user, logout_user
import hashlib

bp_usuario = Blueprint("usuario", __name__, template_folder='templates')

@bp_usuario.route('/recovery')
def recovery():
    dados = Usuario.query.all()
    return render_template('lista_usuarios.html', usuarios=dados)

@bp_usuario.route('/create', methods=['GET', 'POST'])
def create():
    if request.method=="GET":
        return render_template('usuario_create.html')

    if request.method=="POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        md5 = hashlib.md5()
        md5.update(senha.encode('utf-8'))
        senha_cripto = md5.hexdigest()

        email_existente = Usuario.query.filter_by(email=email).first()
        if email_existente:
            flash('Email existente!')
            return render_template('usuario_create.html')
        else:
            u = Usuario(nome, email, senha_cripto)
            db.session.add(u)
            db.session.commit()
            login_user(u)
            return redirect(url_for('usuario.recovery'))
      

@lm.user_loader
def load_user(id):
    usuario = Usuario.query.get(id)
    return usuario

@bp_usuario.route('/autenticar', methods=['POST'])
def autenticar():
    email = request.form['email'] 
    senha = request.form['senha']
    usuario = Usuario.query.filter_by(email=email).first()

    md5 = hashlib.md5()
    md5.update(senha.encode('utf-8'))
    senha_cripto = md5.hexdigest()

    if (usuario and usuario.senha == senha_cripto):
        login_user(usuario)
        return redirect(url_for('usuario.recovery'))
    else:
        flash('Login ou senha incorretos')
        return redirect('/login')

@bp_usuario.route('/logoff')
def logoff():
    logout_user()
    flash('Usuário desconectado do sistema')
    return redirect('/login')