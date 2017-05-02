from app import db

class Clase(db.Model):
    __tablename__ = 'par_tclase'
    cla_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    cla_nombre = db.Column(db.String, nullable = False)
    cla_linea = db.Column(db.Integer, nullable = False)
    cla_tipo = db.Column(db.Integer)


    def __init__(self, cla_id, cla_nombre, cla_linea):
        self.cla_id = cla_id
        self.cla_nombre = cla_nombre
        self.cla_linea = cla_linea

    def __repr__(self):
        texto = '''<cla_nombre: {} >'''
        return texto.format(self.cla_nombre)