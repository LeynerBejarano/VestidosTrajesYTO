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

class Despacho(db.Model):
    __tablename__ = 'neg_tdespacho'
    des_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    des_pedido = db.Column(db.Integer)
    des_prestamo = db.Column(db.Integer)
    des_presindiv = db.Column(db.Integer)
    des_prespedido = db.Column(db.Integer)
    des_fecha = db.Column(db.DateTime)
    des_fecha_entrega = db.Column(db.Date)
    des_hora_entrega = db.Column(db.Time)
    des_observaciones = db.Column(db.String(300))
    des_crea = db.Column(db.String(10))
    des_modifica = db.Column(db.String(10))
    des_fecha_mod = db.Column(db.DateTime)

    def __init__(self, des_pedido, des_prestamo, des_presindiv, des_prespedido, des_fecha_entrega, des_hora_entrega, des_observaciones, des_fecha, des_crea, des_modifica): 
        self.des_pedido = des_pedido
        self.des_prestamo = des_prestamo
        self.des_presindiv = des_presindiv
        self.des_prespedido = des_prespedido
        self.des_fecha = des_fecha
        self.des_fecha_entrega = des_fecha_entrega
        self.des_hora_entrega = des_hora_entrega
        self.des_observaciones = des_observaciones
        self.des_crea = des_crea
        self.des_modifica = des_modifica
        self.des_fecha_mod = datetime.now(timezone('America/Bogota'))

    def __repr__(self):
        texto = '''<des_prestamo: {} >
        <des_presindiv: {} >
        <des_prespedido: {} >'''
        return texto.format(self.des_motivo, self.des_prestamo, self.des_presindiv, self.des_prespedido)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id' : self.des_id,
        'pedido' : self.des_pedido,
        'prestamo' : self.des_prestamo,
        'presindiv' : self.des_presindiv,
        'prespedido' : self.des_prespedido,
        'fecha': to_iso(self.des_fecha),
        'fecha_entrega' : to_iso(self.des_fecha_entrega),
        'hora_entrega' : parse_time(self.des_hora_entrega),
        'observaciones': self.des_observaciones,
        'crea' : self.des_crea,
        'modifica' : self.des_modifica,
        'fecha_mod' : self.des_fecha_mod.isoformat()
       }



