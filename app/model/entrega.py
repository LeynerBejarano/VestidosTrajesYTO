from app import db

class Entrega(db.Model):
    __tablename__ = 'par_tentrega'
    ent_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    ent_nombre = db.Column(db.String, nullable = False)
    ent_val_unitario = db.Column(db.DECIMAL)

    def __init__(self, ent_nombre, ent_val_unitario):
        self.ent_nombre = ent_nombre
        self.ent_val_unitario = ent_val_unitario

    def __repr__(self):
        texto = '''<ent_nombre: {} >'''
        return texto.format(self.ent_nombre)