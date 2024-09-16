from utils import db

class Capitais(db.Model):
  __tablename__= "capitais"
  id = db.Column(db.Integer, primary_key = True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  regiao = db.Column(db.String(100))
  estado = db.Column(db.String(100))
  sigla = db.Column(db.String(100))
  capital = db.Column(db.String(100))

  usuario = db.relationship('Usuario', foreign_keys=id_usuario)

  def __init__(self,id_usuario, regiao, estado, sigla, capital):
    self.id_usuario = id_usuario
    self.regiao = regiao
    self.estado = estado
    self.sigla= sigla
    self.capital = capital

  def __repr__(self):
    return "<Capitais: {} - {} - {} - {}".format(self.regiao, self.estado, self.sigla, self.capital)
