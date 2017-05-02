from app import db
from pytz import timezone
from datetime import datetime

class Det_prospecto(db.Model):
    __tablename__ = 'neg_tdet_prospecto'
    det_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    det_prospecto = db.Column(db.Integer)
    det_clase = db.Column(db.Integer)
    det_color = db.Column(db.Integer)
    det_estilo = db.Column(db.Integer)
    det_detalle = db.Column(db.String(100))
    det_pedida = db.Column(db.Integer)
    det_cortesia = db.Column(db.Integer)
    det_despachada = db.Column(db.Integer)
    det_devuelta = db.Column(db.Integer)
    det_entregada = db.Column(db.Integer)
    det_faltante = db.Column(db.Integer)
    det_recogida = db.Column(db.Integer)
    det_crea = db.Column(db.String(10))
    det_modifica = db.Column(db.String(10))
    det_fecha_mod = db.Column(db.DateTime)

    def __init__(self, det_prospecto, det_clase, det_color, det_estilo, det_detalle, det_pedida, det_cortesia, det_despachada, det_devuelta, det_entregada, det_faltante, det_recogida, det_crea, det_modifica):
        self.det_prospecto = det_prospecto
        self.det_clase = det_clase
        self.det_color = det_color
        self.det_estilo = det_estilo
        self.det_detalle = det_detalle
        self.det_pedida = det_pedida
        self.det_cortesia = det_cortesia
        self.det_despachada = det_despachada
        self.det_devuelta = det_devuelta
        self.det_entregada = det_entregada
        self.det_faltante = det_faltante
        self.det_recogida = det_recogida
        self.det_crea = det_crea
        self.det_modifica = det_modifica
        self.det_fecha_mod = datetime.now(timezone('America/Bogota'))


    def __repr__(self):

        texto = '''<det_id: {} >
        <det_prospecto: {} >
        <det_clase: {} >
        <det_color: {} >
        <det_estilo: {} >
        <det_detalle: {} >
        <det_pedida: {} >
        <det_cortesia: {} >
        <det_despachada: {} >
        <det_devuelta: {} >
        <det_entregada: {} >
        <det_faltante: {} >
        <det_recogida: {} >'''
        return texto.format(self.det_id, self.det_prospecto, self.det_clase, self.det_color, self.det_estilo, self.det_detalle, self.det_pedida, self.det_cortesia, self.det_despachada, self.det_devuelta, self.det_entregada, self.det_faltante, self.det_recogida)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id' : self.det_id,
        'prospecto' : self.det_prospecto,
        'clase' : self.det_clase,
        'color' : self.det_color,
        'estilo' : self.det_estilo,
        'detalle' : self.det_detalle,
        'pedida' : self.det_pedida,
        'cortesia' : self.det_cortesia,
        'despachada' : self.det_despachada,
        'devuelta' : self.det_devuelta,
        'entregada' : self.det_entregada,
        'faltante' : self.det_faltante,
        'recogida' : self.det_recogida,
        'crea' : self.det_crea,
        'modifica' : self.det_modifica,
        'fecha_mod' : self.det_fecha_mod.isoformat()
       }



