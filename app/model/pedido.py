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

class Pedido(db.Model):
    __tablename__ = 'neg_tpedido'
    ped_numero = db.Column(db.Integer, primary_key = True, autoincrement=True)
    ped_empresa = db.Column(db.DECIMAL, nullable = False)
    ped_cliente = db.Column(db.DECIMAL, nullable = False)
    ped_institucion = db.Column(db.DECIMAL, nullable = False)
    ped_fecha = db.Column(db.DateTime)
    ped_total = db.Column(db.DECIMAL)
    ped_evento = db.Column(db.Integer)
    ped_poblacion = db.Column(db.Integer, nullable = False)
    ped_estilo = db.Column(db.String(10))
    ped_jornada = db.Column(db.Integer)
    ped_nivel = db.Column(db.Integer)
    ped_vendedor = db.Column(db.String(10))
    ped_fecha_evento = db.Column(db.Date)
    ped_hora_evento = db.Column(db.Time)
    ped_fecha_entrega = db.Column(db.Date)
    ped_hora_entrega = db.Column(db.Time)
    ped_fecha_recogida = db.Column(db.Date)
    ped_hora_recogida = db.Column(db.Time)
    ped_tipo_entrega_ord = db.Column(db.Integer)
    ped_tipo_recogida_ord = db.Column(db.Integer)
    ped_val_unitario = db.Column(db.DECIMAL, nullable = False)
    ped_abono = db.Column(db.DECIMAL)
    ped_estado_com = db.Column(db.Integer)
    ped_estado_fin = db.Column(db.Integer)
    ped_estado = db.Column(db.Integer)
    ped_observacion = db.Column(db.String(200))
    ped_manual = db.Column(db.Integer)
    ped_principal = db.Column(db.Integer)
    ped_crea = db.Column(db.String(10))
    ped_modifica = db.Column(db.String(10))
    ped_fecha_mod = db.Column(db.DateTime)

    def __init__(self, ped_empresa, ped_cliente, ped_institucion, ped_total, ped_evento, ped_poblacion, ped_estilo, ped_jornada, ped_nivel, ped_vendedor, ped_fecha_evento, ped_hora_evento, ped_fecha_entrega, ped_hora_entrega, ped_fecha_recogida, ped_hora_recogida, ped_tipo_entrega_ord, ped_tipo_recogida_ord, ped_val_unitario, ped_abono, ped_estado_com, ped_estado_fin, ped_estado, ped_observacion, ped_manual, ped_principal, ped_crea, ped_modifica):
        self.ped_empresa= ped_empresa
        self.ped_cliente= ped_cliente
        self.ped_institucion= ped_institucion
        self.ped_fecha= datetime.now(timezone('America/Bogota'))
        self.ped_total= ped_total
        self.ped_evento= ped_evento
        self.ped_poblacion = ped_poblacion
        self.ped_estilo= ped_estilo
        self.ped_jornada= ped_jornada
        self.ped_nivel= ped_nivel
        self.ped_vendedor= ped_vendedor
        self.ped_fecha_evento= ped_fecha_evento
        self.ped_hora_evento= ped_hora_evento
        self.ped_fecha_entrega = ped_fecha_entrega
        self.ped_hora_entrega = ped_hora_entrega
        self.ped_fecha_recogida = ped_fecha_recogida
        self.ped_tipo_entrega_ord = ped_tipo_entrega_ord
        self.ped_tipo_recogida_ord = ped_tipo_recogida_ord
        self.ped_hora_recogida = ped_hora_recogida
        self.ped_val_unitario = ped_val_unitario
        self.ped_abono = ped_abono
        self.ped_estado_com = ped_estado_com
        self.ped_estado_fin = ped_estado_fin
        self.ped_estado = ped_estado
        self.ped_observacion = ped_observacion 
        self.ped_manual = ped_manual
        self.ped_principal = ped_principal
        self.ped_crea= ped_crea
        self.ped_modifica= ped_modifica
        self.ped_fecha_mod= datetime.now(timezone('America/Bogota'))


    def __repr__(self):
        texto = '''<ped_numero: {}>
        <ped_empresa: {}>
        <ped_cliente: {}>
        <ped_institucion: {}>
        <ped_fecha: {}>
        <ped_total: {}>
        <ped_evento: {}>
        <ped_poblacion: {}>
        <ped_estilo: {}>
        <ped_jornada: {}>
        <ped_nivel: {}>
        <ped_vendedor   : {}>'''
        return texto.format(self.ped_numero, self.ped_empresa, self.ped_cliente, self.ped_institucion, self.ped_fecha, self.ped_total, self.ped_evento, self.ped_poblacion, self.ped_estilo, self.ped_jornada, self.ped_nivel, self.ped_vendedor)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'numero': self.ped_numero,
        'empresa': to_float(self.ped_empresa),
        'cliente': to_float(self.ped_cliente),
        'institucion': to_float(self.ped_institucion),
        'fecha': self.ped_fecha.isoformat(),
        'total': to_float(self.ped_total),
        'evento': self.ped_evento,
        'poblacion': self.ped_poblacion,
        'estilo': self.ped_estilo,
        'jornada': self.ped_jornada,
        'nivel': self.ped_nivel,
        'vendedor': self.ped_vendedor,
        'fecha_evento': to_iso(self.ped_fecha_evento),
        'hora_evento': to_iso(self.ped_hora_evento),
        'fecha_entrega': to_iso(self.ped_fecha_entrega),
        'hora_entrega': parse_time(self.ped_hora_entrega),
        'fecha_recogida': to_iso(self.ped_fecha_recogida),
        'hora_recogida': to_iso(self.ped_hora_recogida),
        'tipo_entrega_ord': self.ped_tipo_entrega_ord,
        'tipo_recogida_ord': self.ped_tipo_recogida_ord,
        'crea': self.ped_crea,
        'modifica': self.ped_modifica,
        'fecha_mod': self.ped_fecha_mod.isoformat(),
        'val_unitario': to_float(self.ped_val_unitario),
        'abono': to_float(self.ped_abono),
        'estado_com': self.ped_estado_com,
        'estado_fin': self.ped_estado_fin,
        'estado': self.ped_estado,
        'observacion': self.ped_observacion,
        'manual' : self.ped_manual,
        'principal': self.ped_principal,
       }



