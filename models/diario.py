# É necessário importar a variável DB
from utils import db

class Diario(db.Model):
  __tablename__= "diario"
  id = db.Column(db.Integer, primary_key = True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  titulo = db.Column(db.String(100))
  disciplina = db.Column(db.String(100))

  usuario = db.relationship('Usuario', foreign_keys=id_usuario)
  
  def __init__(self, id_usuario, titulo, disciplina):
    self.id_usuario = id_usuario
    self.titulo = titulo
    self.disciplina = disciplina

  def __repr__(self):
    return "<Diario: {} - {} - {}".format(self.usuario.nome, self.diario.titulo, self.diario.disciplina)


