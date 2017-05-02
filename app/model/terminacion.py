from app import db

class Terminacion(db.Model):
    __tablename__ = 'par_tterminacion'
    ter_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    ter_nombre = db.Column(db.String, nullable = False)

    def __init__(self, ter_nombre):
        self.ter_nombre = ter_nombre

    def __repr__(self):
        texto = '''<ter_nombre: {} >'''
        return texto.format(self.ter_nombre)