from app import db
from pytz import timezone
from datetime import datetime

def to_iso(date):
    try:
        return date.isoformat()
    except AttributeError:
        return None

class Evento(db.Model):
    __tablename__ = 'par_tevento'
    eve_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    eve_nombre = db.Column(db.String(100), nullable = False)
    

    def __init__(self, eve_nombre):
        self.eve_nombre = cli_identificacion 
        
    def __repr__(self):
    
        texto = '''<eve_id: {}>
        <eve_nombre: {}>
       '''
        return texto.format(self.eve_id, self.eve_nombre,)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': int(self.eve_id),
        'nombre': self.eve_nombre,
       }




