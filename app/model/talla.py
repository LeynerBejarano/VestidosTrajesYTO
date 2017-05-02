from app import db

class Talla(db.Model):
    __tablename__ = 'par_ttalla'
    tal_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    tal_nombre = db.Column(db.String, nullable = False)
    tal_tipo = db.Column(db.Integer)

    def __init__(self, tal_id, tal_nombre, tal_tipo):
        self.tal_id = tal_id
        self.tal_nombre = tal_nombre
        self.tal_tipo = tal_tipo

    def __repr__(self):
        texto = '''<tal_nombre: {} >'''
        return texto.format(self.tal_nombre)