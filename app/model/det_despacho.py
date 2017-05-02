from app import db
from pytz import timezone
from datetime import datetime

class Det_despacho(db.Model):
    __tablename__ = 'neg_tdet_despacho'
    tal_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    tal_talla = db.Column(db.Integer)
    tal_cantidad = db.Column(db.Integer)
    tal_despacho = db.Column(db.Integer)
    tal_crea = db.Column(db.String(10))
    tal_modifica = db.Column(db.String(10))
    tal_fecha_mod = db.Column(db.DateTime)

    def __init__(self, tal_talla, tal_cantidad, tal_despacho, tal_crea, tal_modifica):
        self.tal_talla = tal_talla
        self.tal_cantidad = tal_cantidad
        self.tal_despacho = tal_despacho
        self.tal_crea = tal_crea
        self.tal_modifica = tal_modifica
        self.tal_fecha_mod = datetime.now(timezone('America/Bogota'))


    def __repr__(self):
        texto = '''<tal_talla: {} >
                   <tal_cantidad: {} >
                   <tal_despacho: {} >'''
        return texto.format(self.tal_talla, self.tal_cantidad, self.tal_despacho)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': self.tal_id,
        'talla': self.tal_talla,
        'cantidad': self.tal_cantidad,
        'despacho': self.tal_despacho,
        'crea': self.tal_crea,
        'modifica': self.tal_modifica,
        'fecha_mod': self.tal_fecha_mod.isoformat()
       }
