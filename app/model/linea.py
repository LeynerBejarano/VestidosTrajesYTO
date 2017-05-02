from app import db

class Linea(db.Model):
    __tablename__ = 'par_tlinea'
    lin_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    lin_nombre = db.Column(db.String, nullable = False)

    def __init__(self, lin_id, lin_nombre):
        self.lin_id = lin_id
        self.lin_nombre = lin_nombre

    def __repr__(self):
        texto = '''<lin_nombre: {} >'''
        return texto.format(self.lin_nombre)