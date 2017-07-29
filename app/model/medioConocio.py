from app import db
from pytz import timezone
from datetime import datetime


class MedioConocio(db.Model):
    __tablename__ = 'par_tmediocomunicacion'
    medio_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    medio_nombre = db.Column(db.String(100))

    def __init__(self, medio_nombre):
        self.medio_nombre = medio_nombre

    def __repr__(self):
        texto = '''
        <medio_nombre: {}>
       '''
        return texto.format(self.medio_nombre)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'nombre': self.medio_nombre
       }




