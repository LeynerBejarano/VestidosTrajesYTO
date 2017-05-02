from app import db

class Prespedido(db.Model):
    __tablename__ = 'par_tprespedido'
    prp_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    prp_nombre = db.Column(db.String, nullable = False)

    def __init__(self, prp_nombre):
        self.prp_nombre = prp_nombre

    def __repr__(self):
        texto = '''<prp_nombre: {} >'''
        return texto.format(self.prp_nombre)