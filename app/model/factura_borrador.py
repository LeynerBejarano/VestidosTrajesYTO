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

class Factura_Borrador(db.Model):
    __tablename__ = 'neg_tfactura_borrador'
    fac_numero = db.Column(db.Integer, primary_key = True, autoincrement=True)
    fac_borrador = db.Column(db.String(100))
    fac_cliente = db.Column(db.Integer)
    fac_tipoPedido = db.Column(db.Integer, nullable = False)
    fac_ReferenciaNombre = db.Column(db.String(100))
    fac_ReferenciaCelular = db.Column(db.String(100))
    fac_ReferenciaMedio = db.Column(db.Integer)
    fac_poblacion = db.Column(db.String(100))
    fac_evento = db.Column(db.String(100))
    fac_eventoDia = db.Column(db.Integer)
    fac_eventoMes = db.Column(db.Integer)
    fac_eventoAño = db.Column(db.Integer)
    fac_ReferenciaProducto1 = db.Column(db.String(100))
    fac_ReferenciaProducto2 = db.Column(db.String(100))
    fac_ReferenciaProducto3 = db.Column(db.String(100))
    fac_ReferenciaProducto4 = db.Column(db.String(100))
    fac_descripcion1 = db.Column(db.String(200))
    fac_descripcion2 = db.Column(db.String(200))
    fac_descripcion3 = db.Column(db.String(200))
    fac_descripcion4 = db.Column(db.String(200))
    fac_accesorios1 = db.Column(db.String(100))
    fac_accesorios2 = db.Column(db.String(100))
    fac_accesorios3 = db.Column(db.String(100))
    fac_accesorios4 = db.Column(db.String(100))
    fac_MedidasArreglos1 = db.Column(db.String(100))
    fac_MedidasArreglos2 = db.Column(db.String(100))
    fac_MedidasArreglos3 = db.Column(db.String(100))
    fac_MedidasArreglos4 = db.Column(db.String(100))
    fac_ValorReferencia1 = db.Column(db.Integer)
    fac_ValorReferencia2 = db.Column(db.Integer)
    fac_ValorReferencia3 = db.Column(db.Integer)
    fac_ValorReferencia4 = db.Column(db.Integer)
    fac_Total = db.Column(db.Integer)
    fac_Abono = db.Column(db.Integer)
    fac_Saldo = db.Column(db.Integer)
    fac_Retefuente = db.Column(db.Integer)
    fac_ReclamarMercanciaDia = db.Column(db.Integer)
    fac_ReclamarMercanciaMes = db.Column(db.Integer)
    fac_ReclamarMercanciaAño = db.Column(db.Integer)
    fac_DevolverMercanciaDia = db.Column(db.Integer)
    fac_DevolverMercanciaMes = db.Column(db.Integer)
    fac_DevolverMercanciaAño = db.Column(db.Integer)
    fac_AtendidoPor = db.Column(db.String(100))
    fac_modifica = db.Column(db.Integer)
    fac_consecutivoManual = db.Column(db.Integer)
    fac_tipoToga = db.Column(db.Integer)
    fac_colorToga = db.Column(db.Integer)
    fac_nota = db.Column(db.Integer)
    fac_fecha_mod = db.Column(db.DateTime)

    

    def __init__(self,fac_borrador , fac_cliente, fac_tipoPedido, fac_ReferenciaNombre, fac_ReferenciaCelular, fac_ReferenciaMedio, fac_poblacion, fac_evento, fac_eventoDia, fac_eventoMes, fac_eventoAño,  fac_ReferenciaProducto1,  fac_ReferenciaProducto2,  fac_ReferenciaProducto3, fac_ReferenciaProducto4,  fac_descripcion1, fac_descripcion2, fac_descripcion3, fac_descripcion4, fac_accesorios1, fac_accesorios2, fac_accesorios3, fac_accesorios4,  fac_MedidasArreglos1, fac_MedidasArreglos2, fac_MedidasArreglos3, fac_MedidasArreglos4, fac_ValorReferencia1, fac_ValorReferencia2, fac_ValorReferencia3, fac_ValorReferencia4, fac_Total, fac_Abono, fac_Saldo, fac_ReclamarMercanciaDia, fac_ReclamarMercanciaMes, fac_ReclamarMercanciaAño, fac_DevolverMercanciaDia, fac_DevolverMercanciaMes, fac_DevolverMercanciaAño, fac_AtendidoPor, fac_consecutivoManual, fac_nota):
        self.fac_borrador = fac_borrador
        self.fac_tipoPedido= fac_tipoPedido
        self.fac_cliente = fac_cliente
        self.fac_ReferenciaNombre= fac_ReferenciaNombre
        self.fac_ReferenciaCelular= fac_ReferenciaCelular
        self.fac_ReferenciaMedio= fac_ReferenciaMedio
        self.fac_poblacion =  fac_poblacion 
        self.fac_evento = fac_evento
        self.fac_eventoDia = fac_eventoDia
        self.fac_eventoMes = fac_eventoMes
        self.fac_eventoAño  = fac_eventoAño
        self.fac_ReferenciaProducto1 = fac_ReferenciaProducto1
        self.fac_ReferenciaProducto2 = fac_ReferenciaProducto2
        self.fac_ReferenciaProducto3 = fac_ReferenciaProducto3
        self.fac_ReferenciaProducto4 = fac_ReferenciaProducto4
        self.fac_descripcion1 = fac_descripcion1
        self.fac_descripcion2 = fac_descripcion2
        self.fac_descripcion3 = fac_descripcion3
        self.fac_descripcion4 = fac_descripcion4
        self.fac_accesorios1 = fac_accesorios1
        self.fac_accesorios2 = fac_accesorios2
        self.fac_accesorios3 = fac_accesorios3
        self.fac_accesorios4 = fac_accesorios4
        self.fac_MedidasArreglos1 = fac_MedidasArreglos1
        self.fac_MedidasArreglos2 = fac_MedidasArreglos2
        self.fac_MedidasArreglos3 = fac_MedidasArreglos3
        self.fac_MedidasArreglos4 = fac_MedidasArreglos4
        self.fac_ValorReferencia1 = fac_ValorReferencia1
        self.fac_ValorReferencia2 = fac_ValorReferencia2
        self.fac_ValorReferencia3 = fac_ValorReferencia3
        self.fac_ValorReferencia4 = fac_ValorReferencia4
        self.fac_Total = fac_Total
        self.fac_Abono = fac_Abono
        self.fac_Saldo = fac_Saldo
        self.fac_ReclamarMercanciaDia = fac_ReclamarMercanciaDia
        self.fac_ReclamarMercanciaMes = fac_ReclamarMercanciaMes
        self.fac_ReclamarMercanciaAño = fac_ReclamarMercanciaAño
        self.fac_DevolverMercanciaDia = fac_DevolverMercanciaDia
        self.fac_DevolverMercanciaMes = fac_DevolverMercanciaMes
        self.fac_DevolverMercanciaAño = fac_DevolverMercanciaAño
        self.fac_AtendidoPor = fac_AtendidoPor
        #self.fac_modifica = fac_modifica
        self.fac_consecutivoManual = fac_consecutivoManual
        self.fac_nota = fac_nota
        self.fac_fecha_mod = datetime.now(timezone('America/Bogota'))
       


    def __repr__(self):
        texto = '''<fac_numero: {}>
        <fac_borrador : {}>
        <fac_cliente: {}>
        <fac_tipoPedido: {}>
        <fac_ReferenciaNombre: {}>
        <fac_ReferenciaCelular: {}>
        <fac_ReferenciaMedio: {}>
        <fac_poblacion: {}>
        <fac_evento: {}>
        <fac_eventoDia : {}>
        <fac_eventoMes: {}>
        <fac_eventoAño: {}>
        <fac_ReferenciaProducto1: {}>
        <fac_ReferenciaProducto2: {}>
        <fac_ReferenciaProducto3: {}>
        <fac_ReferenciaProducto4: {}>
        <fac_descripcion1: {}>
        <fac_descripcion2: {}>
        <fac_descripcion3: {}>
        <fac_descripcion4: {}>
        <fac_accesorios1: {}>
        <fac_accesorios2: {}>
        <fac_accesorios3: {}>
        <fac_accesorios4: {}>
        <fac_MedidasArreglos1: {}>
        <fac_MedidasArreglos2: {}>
        <fac_MedidasArreglos3: {}>
        <fac_MedidasArreglos4: {}>
        <fac_ValorReferencia1: {}>
        <fac_ValorReferencia2: {}>
        <fac_ValorReferencia3: {}>
        <fac_ValorReferencia4: {}>
        <fac_Total : {}>
        <fac_Abono: {}>
        <fac_Saldo: {}>
        <fac_Retefuente: {}>
        <fac_ReclamarMercanciaDia: {}>
        <fac_ReclamarMercanciaMes: {}>
        <fac_ReclamarMercanciaAño: {}>
        <fac_DevolverMercanciaDia: {}>
        <fac_DevolverMercanciaMes: {}>
        <fac_DevolverMercanciaAño: {}> 
        <fac_AtendioPor: {}>
        <fac_consecutivoManual: {}>
        <fac_tipoToga: {}>
        <fac_colorToga: {}>
        <fac_nota: {}>
        <fac_modifica: {}>
        <fac_fecha_mod: {}>
        '''
        return texto.format(self.fac_borrador, self.fac_tipoPedido, self.fac_cliente, self.fac_ReferenciaNombre,self.fac_ReferenciaCelular,self.fac_ReferenciaMedio,self.fac_poblacion, self.fac_evento, self.fac_eventoDia, self.fac_eventoMes, self.fac_eventoAño, self.fac_ReferenciaProducto1, self.fac_ReferenciaProducto2, self.fac_ReferenciaProducto3, self.fac_ReferenciaProducto4, self.fac_descripcion1, self.fac_descripcion2, self.fac_descripcion3, self.fac_descripcion4, self.fac_accesorios1, self.fac_accesorios2, self.fac_accesorios3, self.fac_accesorios4, self.fac_MedidasArreglos1, self.fac_MedidasArreglos2, self.fac_MedidasArreglos3, self.fac_MedidasArreglos4, self.fac_ValorReferencia1, self.fac_ValorReferencia2, self.fac_ValorReferencia3, self.fac_ValorReferencia4, self.fac_Total, self.fac_Abono, self.fac_Saldo, self.fac_Retefuente, self.fac_ReclamarMercanciaDia, self.fac_ReclamarMercanciaMes, self.fac_ReclamarMercanciaAño, self.fac_DevolverMercanciaDia, self.fac_DevolverMercanciaMes, self.fac_DevolverMercanciaAño, self.fac_AtendioPor, self.fac_consecutivoManual, self.fac_tipoToga, self.fac_colorToga, self.fac_nota)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'numero': self.fac_numero,
        'fac_borrador' : self.fac_borrador,
        'cliente': self.fac_cliente,
        'tipoPedido': self.fac_tipoPedido,
        'ReferenciaNombre': self.fac_ReferenciaNombre,
        'ReferenciaCelular': self.fac_ReferenciaCelular,
        'ReferenciaMedio': self.fac_ReferenciaMedio,
        'poblacion': self.fac_poblacion,
        'evento': self.fac_evento,
        'eventoDia': self.fac_eventoDia,
        'eventoMes': self.fac_eventoMes,
        'eventoAño': self.fac_eventoAño,
        'ReferenciaProducto1': self.fac_ReferenciaProducto1,
        'ReferenciaProducto2': self.fac_ReferenciaProducto2,
        'ReferenciaProducto3': self.fac_ReferenciaProducto3,
        'ReferenciaProducto4': self.fac_ReferenciaProducto4,
        'descripcion1': self.fac_descripcion1,
        'descripcion2': self.fac_descripcion2,
        'descripcion3': self.fac_descripcion3,
        'descripcion4': self.fac_descripcion4,
        'accesorios1': self.fac_accesorios1,
        'accesorios2': self.fac_accesorios2,
        'accesorios3': self.fac_accesorios3,
        'accesorios4': self.fac_accesorios4,
        'MedidasArreglos1': self.fac_MedidasArreglos1,
        'MedidasArreglos2': self.fac_MedidasArreglos2,
        'MedidasArreglos3': self.fac_MedidasArreglos3,
        'MedidasArreglos4': self.fac_MedidasArreglos4,
        'ValorReferencia1': self.fac_ValorReferencia1,
        'ValorReferencia2': self.fac_ValorReferencia2,
        'ValorReferencia3': self.fac_ValorReferencia3,
        'ValorReferencia4': self.fac_ValorReferencia4,
        'Total': self.fac_Total,
        'Abono': self.fac_Abono,
        'Saldo': self.fac_Saldo,
        'Retefuente': self.fac_Retefuente,
        'ReclamarMercanciaDia': self.fac_ReclamarMercanciaDia,
        'ReclamarMercanciaMes': self.fac_ReclamarMercanciaMes,
        'ReclamarMercanciaAño': self.fac_ReclamarMercanciaAño,
        'DevolverMercanciaDia': self.fac_DevolverMercanciaDia,
        'DevolverMercanciaMes': self.fac_DevolverMercanciaMes,
        'DevolverMercanciaAño': self.DevolverMercanciaAño,
        'AtendioPor': self.fac_AtendioPor,
        'fac_consecutivoManual' : self.fac_consecutivoManual,
        'fac_tipoToga' : self.fac_tipoToga,
        'fac_colorToga' : self.fac_colorToga,
        'fac_nota' : self.fac_nota
       }
       


