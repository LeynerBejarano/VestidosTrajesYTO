from app import db
from pytz import timezone
from datetime import datetime


class Evento(db.Model):
    __tablename__ = 'par_tevento'
    eve_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    eve_nombre = db.Column(db.String(100))
    

    def __init__(self, eve_nombre):
        self.eve_nombre = eve_nombre 
        
    def __repr__(self):
        texto = '''
        <eve_nombre: {}>
       '''
        return texto.format(self.eve_nombre)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'nombre': self.eve_nombre
       }




