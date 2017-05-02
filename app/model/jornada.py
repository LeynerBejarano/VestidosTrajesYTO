from app import db

class Jornada(db.Model):
    __tablename__ = 'par_tjornada'
    jor_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    jor_nombre = db.Column(db.String, nullable = False)

    def __init__(self, jor_nombre):
        self.jor_nombre = jor_nombre

    def __repr__(self):
        texto = '''<jor_nombre: {} >'''
        return texto.format(self.jor_nombre)