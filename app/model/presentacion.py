from app import db

class Presentacion(db.Model):
    __tablename__ = 'par_tpresentacion'
    prs_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    prs_nombre = db.Column(db.String, nullable = False)

    def __init__(self, prs_nombre):
        self.prs_nombre = prs_nombre

    def __repr__(self):
        texto = '''<prs_nombre: {} >'''
        return texto.format(self.prs_nombre)