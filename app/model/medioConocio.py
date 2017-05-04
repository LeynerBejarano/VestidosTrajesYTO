from app import db
from pytz import timezone
from datetime import datetime

def to_iso(date):
    try:
        return date.isoformat()
    except AttributeError:
        return None

class MedioConocio(db.Model):
    __tablename__ = 'par_tMedioComunicacion'
    medio_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    medio_nombre = db.Column(db.String(200))

    def __init__(self, medio_nombre):
        self.medio_nombre = medio_nombre



    def __repr__(self):
    
        texto = '''<medio_id : {}>
        <medio_nombre: {}>
       '''
        return texto.format(self.medio_id, self.medio_nombre)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': int(self.medio_id),
        'nombre': self.medio_nombre,
       }




