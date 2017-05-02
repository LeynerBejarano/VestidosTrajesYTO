from app import db

class Tipo(db.Model):
    __tablename__ = 'par_ttipo'
    tip_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    tip_nombre = db.Column(db.String, nullable = False)

    def __init__(self, tip_nombre):
        self.tip_nombre = tip_nombre

    def __repr__(self):
        texto = '''<tip_nombre: {} >'''
        return texto.format(self.tip_nombre)