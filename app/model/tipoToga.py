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

class TipoToga(db.Model):
    __tablename__ = 'par_ttipoToga'
    tipoToga_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    tipoToga_nombre = db.Column(db.String(40), nullable = False)
    
    

    def __init__(self, tipoToga_id, tipoToga_nombre,):
        self.tipoToga_id= tipoToga_id
        self.tipoToga_nombre= tipoToga_nombre
               


    def __repr__(self):
        texto = '''<tipoToga_id: {}>
        <tipoToga_nombre: {}>
        '''
        return texto.format(self.tipoToga_id, self.tipoToga_nombre )

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'tipoToga_id': self.tipoToga_id,
        'tipoToga_nombre': self.tipoToga_nombre,
       }
       


