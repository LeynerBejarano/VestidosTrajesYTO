from app import db
from pytz import timezone
from datetime import datetime

class Ciudad(db.Model):
    __tablename__ = 'gen_tciudad'
    ciu_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    ciu_nombre = db.Column(db.String, nullable = False)
    ciu_departamento = db.Column(db.Integer)
    ciu_estado = db.Column(db.Integer)
    ciu_metropol = db.Column(db.Integer)
    ciu_crea = db.Column(db.String(10))
    ciu_modifica = db.Column(db.String(10))
    ciu_fecha_mod = db.Column(db.DateTime)


    def __init__(self, ciu_nombre,ciu_departamento, ciu_estado, ciu_metropol, ciu_crea, ciu_modifica):
        self.ciu_nombre = ciu_nombre
        self.ciu_departamento = ciu_departamento 
        self.ciu_estado = ciu_estado 
        self.ciu_metropol = ciu_metropol 
        self.ciu_crea = ciu_crea 
        self.ciu_modifica = ciu_modifica 
        self.ciu_fecha_mod = datetime.now(timezone('America/Bogota'))


    def __repr__(self):
        texto = '''<ciu_nombre: {} >'''
        return texto.format(self.ciu_nombre)