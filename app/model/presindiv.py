from app import db

class Presindiv(db.Model):
    __tablename__ = 'par_tpresindiv'
    pri_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    pri_nombre = db.Column(db.String, nullable = False)

    def __init__(self, pri_nombre):
        self.pri_nombre = pri_nombre

    def __repr__(self):
        texto = '''<pri_nombre: {} >'''
        return texto.format(self.pri_nombre)