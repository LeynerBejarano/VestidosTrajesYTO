from app import db

class Evento(db.Model):
    __tablename__ = 'par_tevento'
    eve_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    eve_nombre = db.Column(db.String, nullable = False)

    def __init__(self, eve_nombre):
        self.eve_nombre = eve_nombre

    def __repr__(self):
        texto = '''<eve_nombre: {} >'''
        return texto.format(self.eve_nombre)