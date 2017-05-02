from app import db

class Estado_com(db.Model):
    __tablename__ = 'par_testado_com'
    esc_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    esc_nombre = db.Column(db.String, nullable = False)

    def __init__(self, esc_nombre):
        self.esc_nombre = esc_nombre

    def __repr__(self):
        texto = '''<esc_nombre: {} >'''
        return texto.format(self.esc_nombre)