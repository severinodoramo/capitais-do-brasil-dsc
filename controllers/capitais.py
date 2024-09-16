from flask import render_template, request, redirect, flash, url_for
from utils import db
from models.capitais import Capitais
from flask import Blueprint
from flask_login import login_required, current_user

bp_capitais = Blueprint("capitais", __name__, template_folder='templates')

@bp_capitais.route('/recovery', methods=['POST'])
@login_required
def recovery():
    id_usuario = current_user.id
    capitais = Capitais.query.filter_by(id_usuario=id_usuario)
    return render_template('buscar.html', capitais=capitais)

@bp_capitais.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method=="GET":
        if current_user.is_authenticated:
	        return render_template('cadastrar_capitais.html')

    if request.method=="POST":
        id_usuario = current_user.id
        regiao = request.form['regiao']
        estado = request.form['estado']
        sigla = request.form['sigla']
        capital = request.form['capital']
        d = Capitais(id_usuario,regiao,estado,sigla,capital)
        db.session.add(d)
        db.session.commit()
        return render_template("buscar.html")

@bp_capitais.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    capital = Capitais.query.filter_by(id=id, id_usuario=current_user.id).first()

    if request.method=="GET":
        return render_template('capital_editar.html', capital=capital)

    if request.method=="POST":
        capital.regiao = request.form['regiao']
        capital.estado = request.form['estado']
        capital.sigla = request.form['sigla']
        capital.capital = request.form['capital']
        db.session.add(capital)
        db.session.commit()
        return render_template('buscar.html')

@bp_capitais.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    capital = Capitais.query.filter_by(id=id, id_usuario=current_user.id).first()
    db.session.delete(capital)
    db.session.commit()
    return render_template('buscar.html')


    



