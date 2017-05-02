from app import db

class Nivele(db.Model):
    __tablename__ = 'par_tnivele'
    niv_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    niv_nombre = db.Column(db.String, nullable = False)

    def __init__(self, niv_nombre):
        self.niv_nombre = niv_nombre

    def __repr__(self):
        texto = '''<niv_nombre: {} >'''
        return texto.format(self.niv_nombre)