from app import db
from pytz import timezone
from datetime import datetime

def to_float(value):
    try:
        return float(value)
    except TypeError:
        return None

class Empresa(db.Model):
    __tablename__ = 'gen_tempresa'
    emp_nit = db.Column(db.DECIMAL, primary_key = True)
    emp_dv = db.Column(db.DECIMAL)
    emp_nombre = db.Column(db.String, nullable = False)
    emp_razon1 = db.Column(db.String)
    emp_razon2 = db.Column(db.String)
    emp_resolucion = db.Column(db.DECIMAL)
    emp_regimen = db.Column(db.String)
    emp_direccion = db.Column(db.String)
    emp_telefono = db.Column(db.String)
    emp_movil = db.Column(db.String)
    emp_correo = db.Column(db.String)
    emp_ciudad = db.Column(db.Integer)
    emp_barrio = db.Column(db.String(50))
    emp_crea = db.Column(db.String)
    emp_modifica = db.Column(db.String)
    emp_fecha_mod = db.Column(db.DateTime)



    def __init__(self, emp_nit, emp_dv, emp_nombre, emp_razon1, emp_razon2, emp_resolucion, emp_regimen, emp_direccion, emp_telefono, emp_movil, emp_correo, emp_ciudad, emp_barrio, emp_crea, emp_modifica, emp_fecha_mod):
        self.emp_nit = emp_nit
        self.emp_dv = emp_dv
        self.emp_nombre = emp_nombre
        self.emp_razon1 = emp_razon1
        self.emp_razon2 = emp_razon2
        self.emp_resolucion = emp_resolucion
        self.emp_regimen = emp_regimen
        self.emp_direccion = emp_direccion
        self.emp_telefono = emp_telefono
        self.emp_movil = emp_movil
        self.emp_correo = emp_correo
        self.emp_ciudad = emp_ciudad
        self.emp_barrio = emp_barrio
        self.emp_crea = emp_crea
        self.emp_modifica = emp_modifica
        self.emp_fecha_mod = datetime.now(timezone('America/Bogota'))

    def __repr__(self):
        texto = '''<emp_nit: {} >
           <emp_dv: {} >
           <emp_nombre: {} >
           <emp_razon1: {} >
           <emp_razon2: {} >
           <emp_resolucion: {} >
           <emp_regimen: {} >
           <emp_direccion: {} >
           <emp_telefono: {} >
           <emp_movil: {} >
           <emp_correo: {} >
           <emp_ciudad: {} >
           <emp_barrio: {} >'''
        return texto.format(self.emp_nit, self.emp_dv, self.emp_nombre, self.emp_razon1, self.emp_razon2, self.emp_resolucion, self.emp_regimen, self.emp_direccion, self.emp_telefono, self.emp_movil, self.emp_correo, self.emp_ciudad, self.emp_barrio)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
            'nit': to_float(self.emp_nit),
            'dv': to_float(self.emp_dv),
            'nombre': self.emp_nombre,
            'razon1': self.emp_razon1,
            'razon2': self.emp_razon2,
            'resolucion': to_float(self.emp_resolucion),
            'regimen': self.emp_regimen,
            'direccion': self.emp_direccion,
            'telefono': self.emp_telefono,
            'movil': self.emp_movil,
            'correo': self.emp_correo,
            'ciudad': self.emp_ciudad,
            'barrio': self.emp_barrio,
            'crea': self.emp_crea,
            'modifica': self.emp_modifica,
            'fecha_mod': self.emp_fecha_mod.isoformat(),
       }
