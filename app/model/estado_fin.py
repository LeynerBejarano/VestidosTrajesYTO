from app import db

class Estado_fin(db.Model):
    __tablename__ = 'par_testado_fin'
    esf_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    esf_nombre = db.Column(db.String, nullable = False)

    def __init__(self, esf_nombre):
        self.esf_nombre = esf_nombre

    def __repr__(self):
        texto = '''<esf_nombre: {} >'''
        return texto.format(self.esf_nombre)