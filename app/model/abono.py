from app import db
from pytz import timezone
from datetime import datetime

def to_iso(date):
    try:
        return date.isoformat()
    except AttributeError:
        return None


class Abono(db.Model):
    __tablename__ = 'neg_tabono'
    abo_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    abo_pedido = db.Column(db.Integer, nullable = False)
    abo_valor = db.Column(db.DECIMAL, nullable = False)
    abo_tipo = db.Column(db.Integer)
    abo_fecha = db.Column(db.Date)
    abo_observacion = db.Column(db.String)
    abo_crea = db.Column(db.String)
    abo_modifica = db.Column(db.String)
    abo_fecha_mod = db.Column(db.DateTime)


    def __init__(self, abo_pedido, abo_valor, abo_tipo, abo_fecha, abo_observacion, abo_crea, abo_modifica):
        self.abo_pedido = abo_pedido 
        self.abo_valor = abo_valor 
        self.abo_tipo = abo_tipo
        self.abo_fecha = abo_fecha
        self.abo_observacion = abo_observacion
        self.abo_crea = abo_crea 
        self.abo_modifica = abo_modifica 
        self.abo_fecha_mod = datetime.now(timezone('America/Bogota'))


    def __repr__(self):
        texto = '''<abo_id: {}>
                   <abo_tipo: {}>
                   <abo_fecha: {}>
                   <abo_pedido: {}>
                   <abo_valor: {}>
                   <abo_observacion: {}>
                   <abo_crea: {}>
                   <abo_modifica: {}>'''
        return texto.format(self.abo_id, self.abo_tipo, self.abo_fecha, self.abo_pedido, self.abo_valor, self.abo_observacion, self.abo_crea, self.abo_modifica)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': self.abo_id,
        'pedido': self.abo_pedido,
        'valor': self.abo_valor,
        'tipo': self.abo_tipo,
        'fecha': to_iso(self.abo_fecha),
        'observacion': self.abo_observacion,
        'crea': self.abo_crea,
        'modifica': self.abo_modifica,
        'fecha_mod': to_iso(self.abo_fecha_mod)
       }