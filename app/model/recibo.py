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

class Recibo(db.Model):
    __tablename__ = 'neg_trecibo'
    reci_numero = db.Column(db.Integer, primary_key = True, autoincrement=True)
    reci_Factura = db.Column(db.Integer)
    reci_valor = db.Column(db.Integer, nullable = False)
    reci_ciudad = db.Column(db.String(110))
    reci_fecha = db.Column(db.DateTime)
    reci_Total = db.Column(db.Integer)
    reci_AporteEnLetras = db.Column(db.String(500))
    reci_Concepto = db.Column(db.String(100))
    reci_FacturaTipo = db.Column(db.String(100))
    reci_nuevoSaldo = db.Column(db.Integer)
    reci_CCNit = db.Column(db.Integer)
    reci_RecibimosDe = db.Column(db.String(200))
    
    

    def __init__(self, reci_Factura, reci_valor, reci_ciudad, reci_fecha, reci_Total, reci_AporteEnLetras, reci_Concepto,  reci_FacturaTipo, reci_nuevoSaldo, reci_CCNit, reci_reci_RecibimosDe ):
        self.reci_Factura = reci_Factura
        self.reci_valor = reci_valor
        self.reci_ciudad = reci_ciudad
        self.reci_fecha = reci_fecha
        self.reci_Total = reci_Total
        self.reci_AporteEnLetras =  reci_AporteEnLetras 
        self.reci_Concepto = reci_Concepto
        self.reci_FacturaTipo = reci_FacturaTipo
        self.reci_nuevoSaldo = reci_nuevoSaldo
        self.reci_CCNit  = reci_CCNit
        self.reci_RecibimosDe = reci_reci_RecibimosDe
       


    def __repr__(self):
        texto = '''<reci_numero: {}>
        <reci_Factura: {}>
        <reci_valor: {}>
        <reci_ciudad: {}>
        <reci_fecha: {}>
        <reci_Total: {}>
        <reci_AporteEnLetras: {}>
        <reci_Concepto: {}>
        <reci_FacturaTipo : {}>
        <reci_nuevoSaldo: {}>
        <reci_CCNit: {}>
        <reci_RecibimosDe>
        '''
        return texto.format(self.reci_numero , self.reci_Factura, self.reci_valor, self.reci_ciudad, self.reci_fecha, self.reci_Total, self.reci_AporteEnLetras, self.reci_Concepto, self.reci_FacturaTipo, self.reci_nuevoSaldo, self.reci_CCNit, self.reci_RecibimosDe)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'numero': self.reci_numero,
        'factura': self.reci_Factura,
        'valor': self.reci_valor,
        'ciudad': self.reci_ciudad,
        'fecha': self.reci_fecha,
        'total': self.reci_Total,
        'aporteEnLetras': self.reci_AporteEnLetras,
        'concepto': self.reci_Concepto,
        'facturaTipo': self.reci_FacturaTipo,
        'nuevoSaldo': self.reci_nuevoSaldo,
        'CCNit': self.reci_CCNit,
        'RecibimosDe':self.reci_RecibimosDe
       }
       


