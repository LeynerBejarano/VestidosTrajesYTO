from app import db
from pytz import timezone
from datetime import datetime

def to_float(value):
    try:
        return float(value)
    except TypeError:
        return None

def to_iso(date):
    try:
        return date.isoformat()
    except AttributeError:
        return None

class Institucion(db.Model):
    __tablename__ = 'gen_tinstitucion'
    ins_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    ins_nit = db.Column(db.DECIMAL)
    ins_nombre = db.Column(db.String(200))
    ins_ciudad = db.Column(db.Integer, nullable = False)
    ins_crea = db.Column(db.String(10))
    ins_modifica = db.Column(db.String(10))
    ins_fecha_mod = db.Column(db.DateTime)
    
    def __init__(self, ins_nit, ins_nombre, ins_ciudad, ins_crea, ins_modifica): 
        self.ins_nit = ins_nit
        self.ins_nombre = ins_nombre
        self.ins_ciudad = ins_ciudad
        self.ins_crea = ins_crea
        self.ins_modifica = ins_modifica
        self.ins_fecha_mod = datetime.now(timezone('America/Bogota'))


    def __repr__(self):

        texto ='''<ins_nit: {} >
        <ins_nombre: {} >'''
        return texto.format(self.ins_nit, self.ins_nombre)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'nit': to_float(self.ins_nit),
        'nombre': self.ins_nombre,
        'ciudad': self.ins_ciudad,
        'crea': self.ins_crea,
        'modifica': self.ins_modifica,
        'fecha_mod': to_iso(self.ins_fecha_mod)
       }


