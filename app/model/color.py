from app import db

class Color(db.Model):
    __tablename__ = 'par_tcolor'
    col_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    col_nombre = db.Column(db.String, nullable = False)
    col_clase = db.Column(db.Integer)

    def __init__(self, col_nombre, col_clase):
        self.col_nombre = col_nombre
        self.col_clase = col_clase

    def __repr__(self):
        texto = '''<col_nombre: {} >'''
        return texto.format(self.col_nombre)