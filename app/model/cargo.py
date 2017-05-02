from app import db

class Cargo(db.Model):
    __tablename__ = 'par_tcargo'
    crg_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    crg_descripcion = db.Column(db.String, nullable = False)

    def __init__(self, crg_descripcion):
        self.crg_descripcion = crg_descripcion

    def __repr__(self):
        texto = '''<crg_descripcion: {} >'''
        return texto.format(self.crg_descripcion)