from app import db
from pytz import timezone
from datetime import datetime

def to_iso(date):
    try:
        return date.isoformat()
    except AttributeError:
        return None

class Accesorio(db.Model):
    __tablename__ = 'neg_taccesorio'
    acc_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    acc_clase = db.Column(db.Integer)
    acc_color = db.Column(db.Integer)
    acc_estilo = db.Column(db.Integer)
    acc_nombre = db.Column(db.String, nullable = False)
    acc_linea = db.Column(db.Integer)
    acc_cantidad = db.Column(db.Integer)
    acc_val_unitario = db.Column(db.DECIMAL)
    acc_crea = db.Column(db.String(10))
    acc_modifica = db.Column(db.String(10))
    acc_fecha_mod = db.Column(db.DateTime)

    def __init__(self, acc_nombre, acc_linea, acc_color, acc_estilo, acc_clase, acc_cantidad, acc_val_unitario, acc_crea, acc_modifica): 
        self.acc_nombre = acc_nombre
        self.acc_cantidad = acc_cantidad
        self.acc_linea = acc_linea
        self.acc_color = acc_color
        self.acc_estilo = acc_estilo
        self.acc_clase = acc_clase
        self.acc_val_unitario = acc_val_unitario
        self.acc_crea = acc_crea
        self.acc_modifica = acc_modifica
        self.acc_fecha_mod = datetime.now(timezone('America/Bogota'))


    def __repr__(self):
        texto = '''<acc_nombre: {} >
        <acc_cantidad: {} >
        <acc_linea: {} >
        <acc_color: {} >
        <acc_estilo: {} >
        <acc_clase: {} >
        <acc_crea: {} >
        <acc_modifica: {} >
        <acc_fecha_mod: {} >'''
        return texto.format(self.acc_nombre, self.acc_cantidad, self.acc_linea, self.acc_color, self.acc_estilo, self.acc_clase, self.acc_crea, self.acc_modifica, self.acc_fecha_mod)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': self.acc_id,
        'clase': self.acc_clase,
        'color': self.acc_color,
        'estilo': self.acc_estilo,
        'linea': self.acc_linea,
        'nombre': self.acc_nombre,
        'cantidad': self.acc_cantidad,
        'val_unitario': float(self.acc_val_unitario),
        'crea': self.acc_crea,
        'modifica': self.acc_modifica,
        'fecha_mod': to_iso(self.acc_fecha_mod)
       }


