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

class Factura(db.Model):
    __tablename__ = 'neg_tfactura'
    fac_numero = db.Column(db.Integer, primary_key = True, autoincrement=True)
    fac_cliente = db.Column(db.Integer)
    fac_tipoPedido = db.Column(db.Integer, nullable = False)
    fac_ReferenciaNombre = db.Column(db.String(100))
    fac_ReferenciaCelular = db.Column(db.String(100))
    fac_ReferenciaMedio = db.Column(db.Integer)
    fac_poblacion = db.Column(db.String(100))
    fac_evento = db.Column(db.String(100))
    fac_eventoFecha = db.Column(db.DateTime)
    fac_eventoDia = db.Column(db.Integer)
    fac_eventoMes = db.Column(db.Integer)
    fac_eventoAño = db.Column(db.Integer)
    fac_Total = db.Column(db.Integer)
    fac_Saldo = db.Column(db.Integer)
    fac_Retefuente = db.Column(db.Integer)
    fac_ReclamarMercanciaFecha = db.Column(db.DateTime)
    fac_horasReclamarCadaH = db.Column(db.Integer)
    fac_horasCadaReclamarMH =  db.Column(db.Float)
    fac_NombreCliente = db.Column(db.String(200))
    fac_ReclamarMercanciaMes = db.Column(db.Integer)
    fac_ReclamarMercanciaAño = db.Column(db.Integer)
    fac_horasDevolverCadaH = db.Column(db.Integer)
    fac_horasCadaDevolverMH = db.Column(db.Float)
    fac_DevolverMercanciaDia = db.Column(db.Integer)
    fac_DevolverMercanciaMes = db.Column(db.Integer)
    fac_DevolverMercanciaAño = db.Column(db.Integer)
    fac_DevolverMercanciaFecha = db.Column(db.DateTime)
    fac_AtendidoPor = db.Column(db.String(100))
    fac_modifica = db.Column(db.Integer)
    fac_consecutivoManual = db.Column(db.Integer)
    fac_tipoToga = db.Column(db.Integer)
    fac_colorToga = db.Column(db.Integer)
    fac_nota = db.Column(db.Integer)
    fac_fechaFactura = db.Column(db.DateTime)
    fac_fecha_mod = db.Column(db.DateTime)

    

    def __init__(self, fac_cliente, fac_tipoPedido, fac_ReferenciaNombre, fac_ReferenciaCelular, fac_ReferenciaMedio, fac_poblacion, fac_evento, fac_eventoFecha,  fac_eventoDia, fac_eventoMes, fac_eventoAño, fac_Total,  fac_Saldo, fac_Retefuente, fac_ReclamarMercanciaFecha, fac_horasReclamarCadaH, fac_horasCadaReclamarMH,  fac_NombreCliente, fac_ReclamarMercanciaMes, fac_ReclamarMercanciaAño, fac_horasDevolverCadaH, fac_DevolverMercanciaFecha,fac_horasCadaDevolverMH, fac_DevolverMercanciaDia, fac_DevolverMercanciaMes, fac_DevolverMercanciaAño, fac_AtendidoPor, fac_consecutivoManual, fac_nota):
        self.fac_tipoPedido= fac_tipoPedido
        self.fac_cliente = fac_cliente
        self.fac_ReferenciaNombre= fac_ReferenciaNombre
        self.fac_ReferenciaCelular= fac_ReferenciaCelular
        self.fac_ReferenciaMedio= fac_ReferenciaMedio
        self.fac_poblacion =  fac_poblacion 
        self.fac_evento = fac_evento
        self.fac_eventoFecha = fac_eventoFecha
        self.fac_eventoDia = fac_eventoDia
        self.fac_eventoMes = fac_eventoMes
        self.fac_eventoAño  = fac_eventoAño
        self.fac_Total = fac_Total
        self.fac_Saldo = fac_Saldo
        self.fac_Retefuente = fac_Retefuente
        self.fac_ReclamarMercanciaFecha = fac_ReclamarMercanciaFecha
        self.fac_horasReclamarCadaH = fac_horasReclamarCadaH
        self.fac_horasCadaReclamarMH = fac_horasCadaReclamarMH
        self.fac_NombreCliente = fac_NombreCliente
        self.fac_ReclamarMercanciaMes = fac_ReclamarMercanciaMes
        self.fac_ReclamarMercanciaAño = fac_ReclamarMercanciaAño
        self.fac_horasDevolverCadaH = fac_horasDevolverCadaH
        self.fac_horasCadaDevolverMH = fac_horasCadaDevolverMH
        self.fac_DevolverMercanciaDia = fac_DevolverMercanciaDia
        self.fac_DevolverMercanciaMes = fac_DevolverMercanciaMes
        self.fac_DevolverMercanciaAño = fac_DevolverMercanciaAño
        self.fac_DevolverMercanciaFecha = fac_DevolverMercanciaFecha
        self.fac_AtendidoPor = fac_AtendidoPor
        #self.fac_modifica = fac_modifica
        self.fac_consecutivoManual = fac_consecutivoManual
        self.fac_fechaFactura = datetime.now(timezone('America/Bogota'))
        self.fac_nota = fac_nota
        self.fac_fecha_mod = datetime.now(timezone('America/Bogota'))
       


    def __repr__(self):
        texto = '''<fac_numero: {}>
        <fac_cliente: {}>
        <fac_tipoPedido: {}>
        <fac_ReferenciaNombre: {}>
        <fac_ReferenciaCelular: {}>
        <fac_ReferenciaMedio: {}>
        <fac_poblacion: {}>
        <fac_evento: {}>
        <fac_eventoFecha: {}>
        <fac_eventoDia : {}>
        <fac_eventoMes: {}>
        <fac_eventoAño: {}>
        <fac_Total : {}>
        <fac_Saldo: {}>
        <fac_Retefuente: {}>
        <fac_ReclamarMercanciaFecha: {}>
        <fac_horasReclamarCadaH: {}>
        <fac_horasCadaReclamarMH: {}>
        <fac_NombreCliente: {}>
        <fac_ReclamarMercanciaMes: {}>
        <fac_ReclamarMercanciaAño: {}>
        <fac_horasDevolverCadaH:{}>
        <fac_horasCadaDevolverMH: {}>
        <fac_DevolverMercanciaDia: {}>
        <fac_DevolverMercanciaMes: {}>
        <fac_DevolverMercanciaAño: {}>
        <fac_DevolverMercanciaFecha: {}> 
        <fac_AtendioPor: {}>
        <fac_consecutivoManual: {}>
        <fac_tipoToga: {}>
        <fac_colorToga: {}>
        <fac_nota: {}>
        <fac_modifica: {}>
        <fac_fechaFactura: {}>
        <fac_fecha_mod: {}>
        '''
        return texto.format(self.fac_tipoPedido, self.fac_cliente, self.fac_ReferenciaNombre,self.fac_ReferenciaCelular,self.fac_ReferenciaMedio,self.fac_poblacion, self.fac_evento, self.fac_eventoFecha, self.fac_eventoDia, self.fac_eventoMes, self.fac_eventoAño, self.fac_Total, self.fac_Saldo, self.fac_Retefuente, self.fac_ReclamarMercanciaFecha, self.fac_horasReclamarCadaH,self.fac_horasCadaReclamarMH, self.fac_NombreCliente, self.fac_ReclamarMercanciaMes, self.fac_ReclamarMercanciaAño, self.fac_DevolverMercanciaDia, self.fac_DevolverMercanciaMes, self.fac_DevolverMercanciaAño, self.fac_DevolverMercanciaFecha, self.fac_AtendioPor, self.fac_consecutivoManual, self.fac_tipoToga, self.fac_colorToga,self.fac_fechaFactura, self.fac_nota)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'numero': self.fac_numero,
        'cliente': self.fac_cliente,
        'tipoPedido': self.fac_tipoPedido,
        'ReferenciaNombre': self.fac_ReferenciaNombre,
        'ReferenciaCelular': self.fac_ReferenciaCelular,
        'ReferenciaMedio': self.fac_ReferenciaMedio,
        'poblacion': self.fac_poblacion,
        'evento': self.fac_evento,
        'eventoFecha': self.fac_eventoFecha,
        'eventoDia': self.fac_eventoDia,
        'eventoMes': self.fac_eventoMes,
        'eventoAño': self.fac_eventoAño,
        'Total': self.fac_Total,
        'Saldo': self.fac_Saldo,
        'Retefuente': self.fac_Retefuente,
        'ReclamarMercanciaFecha': self.fac_ReclamarMercanciaFecha,
        'fac_horasReclamarCadaH': self.fac_horasReclamarCadaH,
        'fac_horasCadaReclamarMH': self.fac_horasCadaReclamarMH,
        'NombreCliente': self.fac_NombreCliente,
        'ReclamarMercanciaMes': self.fac_ReclamarMercanciaMes,
        'ReclamarMercanciaAño': self.fac_ReclamarMercanciaAño,
        'fac_horasDevolverCadaH': self.fac_horasDevolverCadaH,
        'fac_horasCadaDevolverMH': self.fac_horasCadaDevolverMH,
        'DevolverMercanciaDia': self.fac_DevolverMercanciaDia,
        'DevolverMercanciaMes': self.fac_DevolverMercanciaMes,
        'DevolverMercanciaAño': self.fac_DevolverMercanciaAño,
        'DevolverMercanciaFecha': self.fac_DevolverMercanciaFecha,
        'AtendioPor': self.fac_AtendioPor,
        'fac_consecutivoManual' : self.fac_consecutivoManual,
        'fac_tipoToga' : self.fac_tipoToga,
        'fac_colorToga' : self.fac_colorToga,
        'fac_fechaFactura': self.fac_fechaFactura,
        'fac_nota' : self.fac_nota
       }
       


