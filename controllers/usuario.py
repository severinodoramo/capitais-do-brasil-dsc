from flask import render_template, request, redirect, flash, url_for
from utils import db, lm
from models.usuario import Usuario
from flask import Blueprint
from flask_login import login_user, logout_user, current_user
import hashlib

bp_usuario = Blueprint("usuario", __name__, template_folder='templates')

@bp_usuario.route('/')
def home():
    return redirect(url_for('usuario.recovery'))

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

        user = Usuario.query.filter_by(email=email).first()
        if user:
            flash('Email já exsite!', category='error')
            return render_template('usuario_create.html')
        elif len(nome) < 3:
            flash('Nome muito pequeno!', category='error')
            return render_template('usuario_create.html')
        elif len(senha) < 8:
            flash('Senha deve ter no mínimo 8 caracteres', category='error')
            return render_template('usuario_create.html')
        else:
            u = Usuario(nome, email, senha_cripto)
            db.session.add(u)
            db.session.commit()
            login_user(u)
            flash('Conta criada com sucesso!', category='success')
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
        flash('Logado com suceso!')
        return redirect(url_for('usuario.recovery'))
    else:
        flash('Login ou senha incorretos')
        return redirect('/login')

@bp_usuario.route('/logoff')
def logoff():
    logout_user()
    flash('Usuário desconectado do sistema')
    return redirect('/login')

@bp_usuario.route('/update', methods=['GET', 'POST'])
def update():
    id_usuario = current_user.id
    usuario = Usuario.query.filter_by(id=id_usuario).first()

    if request.method == 'GET':
        return render_template('usuario_update.html', usuario=usuario)
    
    if request.method=="POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        usuario_atual = Usuario.query.filter_by(id=current_user.id).first()
        email_atual = usuario_atual.email

        md5 = hashlib.md5()
        md5.update(senha.encode('utf-8'))
        senha_cripto = md5.hexdigest()

        user = Usuario.query.filter_by(email=email).first()
        if user and user.email != email_atual:
            flash('Email já exsite!', category='error')
            return redirect(url_for('usuario.update'))
        elif len(nome) < 3:
            flash('Nome muito pequeno!', category='error')
            return redirect(url_for('usuario.update'))
        elif senha_cripto != user.senha:
            flash('Senha incorreta!', category='error')
            return redirect(url_for('usuario.update'))
        else:
            user.nome = nome
            user.email = email
            db.session.commit()
            flash('Conta atualizada com sucesso!', category='success')
            return redirect(url_for('usuario.recovery'))
        
@bp_usuario.route('/delete')
def delete():
    usuario = Usuario.query.filter_by(id=id, id_usuario=current_user.id).first()
    db.session.delete(usuario)
    db.session.commit()
    return render_template('login.html')
