from app import db

class Estilo(db.Model):
    __tablename__ = 'par_testilo'
    est_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    est_nombre = db.Column(db.String, nullable = False)
    est_clase = db.Column(db.Integer)

    def __init__(self, est_id, est_nombre):
        self.est_id = est_id
        self.est_nombre = est_nombre
        self.est_clase = est_clase

    def __repr__(self):
        texto = '''<est_nombre: {} >'''
        return texto.format(self.est_nombre)