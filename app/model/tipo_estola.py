from app import db

class Tipo_estola(db.Model):
    __tablename__ = 'par_ttipo_estola'
    tes_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    tes_nombre = db.Column(db.String, nullable = False)
    tes_val_unitario = db.Column(db.DECIMAL)

    def __init__(self, tes_nombre, tes_val_unitario):
        self.tes_nombre = tes_nombre
        self.tes_val_unitario = tes_val_unitario

    def __repr__(self):
        texto = '''<tes_nombre: {} >'''
        return texto.format(self.tes_nombre)