from app import db
from pytz import timezone
from datetime import datetime


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

class Orden(db.Model):
    __tablename__ = 'neg_torden'
    ord_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    ord_pedido = db.Column(db.Integer, nullable = False)
    ord_despacho = db.Column(db.Integer, nullable = False)
    ord_tipo = db.Column(db.Integer, nullable = False)
    ord_fecha = db.Column(db.Date, nullable = False)
    ord_fecha_evento = db.Column(db.Date, nullable = False)
    ord_hora_evento = db.Column(db.Time)
    ord_hora = db.Column(db.Time)
    ord_personalizada = db.Column(db.Integer)
    ord_transportadora = db.Column(db.Integer)
    ord_observaciones = db.Column(db.String(200))
    ord_tipo_orden = db.Column(db.Integer)
    ord_crea = db.Column(db.String(10))
    ord_modifica = db.Column(db.String(10))
    ord_fecha_mod = db.Column(db.DateTime)

    def __init__(self, ord_pedido, ord_despacho, ord_tipo, ord_fecha, ord_fecha_evento, ord_hora_evento, ord_hora, ord_personalizada, ord_transportadora, ord_observaciones, ord_tipo_orden, ord_crea, ord_modifica): 
        self.ord_pedido = ord_pedido
        self.ord_despacho = ord_despacho
        self.ord_tipo = ord_tipo
        self.ord_fecha = ord_fecha
        self.ord_fecha_evento = ord_fecha_evento
        self.ord_hora_evento = ord_hora_evento
        self.ord_hora = ord_hora
        self.ord_personalizada = ord_personalizada
        self.ord_transportadora = ord_transportadora
        self.ord_observaciones = ord_observaciones
        self.ord_tipo_orden = ord_tipo_orden
        self.ord_crea = ord_crea
        self.ord_modifica = ord_modifica
        self.ord_fecha_mod = datetime.now(timezone('America/Bogota'))

    def __repr__(self):
        texto = '''<ord_id: {}>
                   <ord_pedido: {}>
                   <ord_despacho: {}>
                   <ord_tipo: {}>
                   <ord_fecha: {}>
                   <ord_fecha_evento: {}>
                   <ord_hora_evento: {}>
                   <ord_hora: {}>
                   <ord_personalizada: {}>
                   <ord_transportadora: {}>
                   <ord_observaciones: {}>
                   <ord_tipo_orden: {}'''
        return texto.format(self.ord_id, self.ord_pedido, self.ord_despacho, self.ord_tipo, self.ord_fecha, self.ord_fecha_evento, self.ord_hora_evento, self.ord_hora, self.ord_personalizada, self.ord_transportadora, self.ord_observaciones, self.ord_tipo_orden)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': self.ord_id,
        'pedido': self.ord_pedido,
        'despacho': self.ord_despacho,
        'tipo': self.ord_tipo,
        'fecha': to_iso(self.ord_fecha),
        'fecha_evento': to_iso(self.ord_fecha_evento),
        'hora_evento': to_iso(self.ord_hora_evento),
        'hora': to_iso(self.ord_hora),
        'personalizada': self.ord_personalizada,
        'transportadora': self.ord_transportadora,
        'observaciones': self.ord_observaciones,
        'tipo_orden': self.ord_tipo_orden,
        'crea': self.ord_crea,
        'modifica': self.ord_modifica,
        'fecha_mod': to_iso(self.ord_fecha_mod)
       }



