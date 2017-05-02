from app import db
from pytz import timezone
from datetime import datetime
def to_iso(date):
    try:
        return date.isoformat()
    except AttributeError:
        return None

class Prenda(db.Model):
    __tablename__ = 'neg_tprenda'
    pre_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    pre_clase = db.Column(db.Integer)
    pre_color = db.Column(db.Integer)
    pre_estilo = db.Column(db.Integer)
    pre_linea = db.Column(db.Integer)
    pre_nombre = db.Column(db.String(50), nullable = False)
    pre_cantidad = db.Column(db.Integer)
    pre_piezas = db.Column(db.Integer)
    pre_imagen = db.Column(db.String(300))
    pre_val_unitario = db.Column(db.DECIMAL)
    pre_crea = db.Column(db.String(10))
    pre_modifica = db.Column(db.String(10))
    pre_fecha_mod = db.Column(db.DateTime)

    def __init__(self, pre_nombre, pre_cantidad, pre_piezas, pre_color, pre_clase, pre_estilo, pre_linea, pre_imagen, pre_val_unitario, pre_crea, pre_modifica): 
        self.pre_nombre = pre_nombre
        self.pre_cantidad = pre_cantidad
        self.pre_piezas = pre_piezas
        self.pre_color = pre_color
        self.pre_clase = pre_clase
        self.pre_estilo = pre_estilo
        self.pre_linea = pre_linea
        self.pre_imagen = pre_imagen
        self.pre_val_unitario = pre_val_unitario
        self.pre_crea = pre_crea
        self.pre_modifica = pre_modifica
        self.pre_fecha_mod = datetime.now(timezone('America/Bogota'))


    def __repr__(self):
        texto = '''<pre_nombre: {} >
        <pre_cantidad: {} >
        <pre_piezas: {} >
        <pre_color: {} >
        <pre_clase: {} >
        <pre_estilo: {} >
        <pre_imagen: {} >
        <pre_crea: {} >
        <pre_modifica: {} >
        <pre_fecha_mod: {} >'''
        return texto.format(self.pre_nombre, self.pre_cantidad, self.pre_piezas, self.pre_color, self.pre_clase,  self.pre_estilo, self.pre_imagen, self.pre_crea,   self.pre_modifica, self.pre_fecha_mod)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': self.pre_id,
        'clase': self.pre_clase,
        'color': self.pre_color,
        'estilo': self.pre_estilo,
        'linea': self.pre_linea,
        'nombre': self.pre_nombre,
        'cantidad': self.pre_cantidad,
        'piezas': self.pre_piezas,
        'imagen': self.pre_imagen,
        'val_unitario': float(self.pre_val_unitario),
        'crea': self.pre_crea,
        'modifica': self.pre_modifica,
        'fecha_mod': to_iso(self.pre_fecha_mod)
       }


