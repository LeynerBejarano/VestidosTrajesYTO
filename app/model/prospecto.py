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

def parse_time(time):
    try:
        return time.strftime('%I:%M %p')
    except Exception:
        return None

class Prospecto(db.Model):
    __tablename__ = 'neg_tprospecto'
    pro_numero = db.Column(db.Integer, primary_key = True, autoincrement=True)
    pro_empresa = db.Column(db.DECIMAL, nullable = False)
    pro_cliente = db.Column(db.DECIMAL, nullable = False)
    pro_institucion = db.Column(db.DECIMAL, nullable = False)
    pro_fecha = db.Column(db.DateTime)
    pro_total = db.Column(db.DECIMAL)
    pro_poblacion = db.Column(db.Integer, nullable = False)
    pro_evento = db.Column(db.Integer)
    pro_estilo = db.Column(db.String(10))
    pro_jornada = db.Column(db.Integer)
    pro_nivel = db.Column(db.Integer)
    pro_vendedor = db.Column(db.String(10))
    pro_fecha_evento = db.Column(db.Date)
    pro_hora_evento = db.Column(db.Time)
    pro_fecha_entrega = db.Column(db.Date)
    pro_hora_entrega = db.Column(db.Time)
    pro_fecha_recogida = db.Column(db.Date)
    pro_hora_recogida = db.Column(db.Time)
    pro_tipo_entrega_ord = db.Column(db.Integer)
    pro_tipo_recogida_ord = db.Column(db.Integer)
    pro_val_unitario = db.Column(db.DECIMAL, nullable = False)
    pro_abono = db.Column(db.DECIMAL)
    pro_estado_com = db.Column(db.Integer)
    pro_estado_fin = db.Column(db.Integer)
    pro_estado = db.Column(db.Integer)
    pro_observacion = db.Column(db.String(200))
    pro_fecha_contacto = db.Column(db.Date)
    pro_principal = db.Column(db.Date)
    pro_crea = db.Column(db.String(10))
    pro_modifica = db.Column(db.String(10))
    pro_fecha_mod = db.Column(db.DateTime)

    def __init__(self, pro_empresa, pro_cliente, pro_institucion, pro_total, pro_evento, pro_poblacion, pro_estilo, pro_jornada, pro_nivel, pro_vendedor, pro_fecha_evento, pro_hora_evento, pro_fecha_entrega, pro_hora_entrega, pro_fecha_recogida, pro_hora_recogida, pro_tipo_entrega_ord, pro_tipo_recogida_ord, pro_val_unitario, pro_abono, pro_estado_com, pro_estado_fin, pro_estado, pro_observacion, pro_fecha_contacto, pro_principal, pro_crea, pro_modifica):
        self.pro_empresa= pro_empresa
        self.pro_cliente= pro_cliente
        self.pro_institucion= pro_institucion
        self.pro_fecha= datetime.now(timezone('America/Bogota'))
        self.pro_total= pro_total
        self.pro_evento= pro_event
        self.pro_poblacion = pro_poblacion
        self.pro_estilo= pro_estilo
        self.pro_jornada= pro_jornada
        self.pro_nivel= pro_nivel
        self.pro_vendedor= pro_vendedor
        self.pro_fecha_evento= pro_fecha_evento
        self.pro_hora_evento= pro_hora_evento
        self.pro_fecha_entrega = pro_fecha_entrega
        self.pro_hora_entrega = pro_hora_entrega
        self.pro_fecha_recogida = pro_fecha_recogida
        self.pro_hora_recogida = pro_hora_recogida
        self.pro_tipo_entrega_ord = pro_tipo_entrega_ord
        self.pro_tipo_recogida_ord = pro_tipo_recogida_ord
        self.pro_val_unitario = pro_val_unitario
        self.pro_abono = pro_abono
        self.pro_estado_com = pro_estado_com
        self.pro_estado_fin = pro_estado_fin
        self.pro_estado = pro_estado
        self.pro_observacion = pro_observacion 
        self.pro_fecha_contacto = pro_fecha_contacto
        self.pro_principal = pro_principal
        self.pro_crea= pro_crea
        self.pro_modifica= pro_modifica
        self.pro_fecha_mod= datetime.now(timezone('America/Bogota'))

    def __repr__(self):
        texto = '''<pro_numero: {}>
        <pro_empresa: {}>
        <pro_cliente: {}>
        <pro_institucion: {}>
        <pro_fecha: {}>
        <pro_total: {}>
        <pro_evento: {}>
        <pro_poblacion: {}>
        <pro_estilo: {}>
        <pro_jornada: {}>
        <pro_nivel: {}>
        <pro_vendedor   : {}>
        <pro_fecha_contacto: {}>'''
        return texto.format(self.pro_numero, self.pro_empresa, self.pro_cliente, self.pro_institucion, self.pro_fecha, self.pro_total, self.pro_evento, self.pro_poblacion, self.pro_estilo, self.pro_jornada, self.pro_nivel, self.pro_vendedor, self.pro_fecha_contacto)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'numero': self.pro_numero,
        'empresa': to_float(self.pro_empresa),
        'cliente': to_float(self.pro_cliente),
        'institucion': to_float(self.pro_institucion),
        'fecha': self.pro_fecha.isoformat(),
        'total': to_float(self.pro_total),
        'evento': self.pro_evento,
        'poblacion': self.pro_poblacion,
        'estilo': self.pro_estilo,
        'jornada': self.pro_jornada,
        'nivel': self.pro_nivel,
        'vendedor': self.pro_vendedor,
        'fecha_evento': to_iso(self.pro_fecha_evento),
        'hora_evento': to_iso(self.pro_hora_evento),
        'fecha_entrega': to_iso(self.pro_fecha_entrega),
        'hora_entrega': parse_time(self.pro_hora_entrega),
        'fecha_recogida': to_iso(self.pro_fecha_recogida),
        'hora_recogida': to_iso(self.pro_hora_recogida),
        'tipo_entrega_ord': self.pro_tipo_entrega_ord,
        'tipo_recogida_ord': self.pro_tipo_recogida_ord,
        'crea': self.pro_crea,
        'modifica': self.pro_modifica,
        'fecha_mod': self.pro_fecha_mod.isoformat(),
        'val_unitario': to_float(self.pro_val_unitario),
        'abono': to_float(self.pro_abono),
        'estado_com': self.pro_estado_com,
        'estado_fin': self.pro_estado_fin,
        'estado': self.pro_estado,
        'observacion': self.pro_observacion,
        'fecha_contacto': to_iso(self.pro_fecha_contacto),
        'principal': self.pro_principal,
       }



