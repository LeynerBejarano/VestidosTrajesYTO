from app import db
from pytz import timezone
from datetime import datetime

#falta el dato de la manual 
#falta diferenciar el dia en que se creo del dia de modificacion

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

def parse_time(time):
    try:
        return time.strftime('%I:%M %p')
    except Exception:
        return None

class FacturaDetalle(db.Model):
    __tablename__ = 'neg_facturadetalle'
    facdet_Numero = db.Column(db.Integer, primary_key = True, autoincrement=True)
    facdet_Factura = db.Column(db.Integer)
    facdet_Referencia = db.Column(db.Integer)
    facdet_Descripcion = db.Column(db.String(200))
    facdet_Accesorios = db.Column(db.String(500))
    facdet_MedidasyArreglos = db.Column(db.String(500))
    facdet_estilo = db.Column(db.String(200))
    facdet_precio = db.Column(db.String(200))
    facdet_linea = db.Column(db.String(200))

    

    

    def __init__(self, facdet_Factura,facdet_Referencia,facdet_Descripcion,facdet_Accesorios,facdet_MedidasyArreglos,facdet_estilo,facdet_precio,facdet_linea):
        self.facdet_Factura = facdet_Factura
        self.facdet_Referencia = facdet_Referencia
        self.facdet_Descripcion = facdet_Descripcion
        self.facdet_Accesorios = facdet_Accesorios
        self.facdet_MedidasyArreglos = facdet_MedidasyArreglos
        self.facdet_estilo = facdet_estilo 
        self.facdet_precio = facdet_precio
        self.facdet_linea = facdet_linea
        
       


    def __repr__(self):
        texto = '''<facdet_Factura: {}>
        <facdet_Referencia: {}>
        <facdet_Descripcion: {}>
        <facdet_Accesorios: {}>
        <facdet_MedidasyArreglos: {}>
        <facdet_estilo: {}>
        <facdet_precio: {}>
        <facdet_linea: {}>
               '''
        return texto.format(self.facdet_Factura,self.facdet_Referencia,self.facdet_Descripcion,self.facdet_Accesorios,self.facdet_MedidasyArreglos,self.facdet_estilo,self.facdet_precio,self.facdet_linea)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'numero': self.facdet_Numero,
        'factura': self.facdet_Factura,
        'referencia': self.facdet_Referencia,
        'descripcion': self.facdet_Descripcion,
        'accesorios': self.facdet_Accesorios,
        'medidasYarreglos': self.facdet_MedidasyArreglos,
        'estilo': self.facdet_estilo,
        'precio': self.facdet_precio,
        'linea': self.facdet_linea
       }
       


