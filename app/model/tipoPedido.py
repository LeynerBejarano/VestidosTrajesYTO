from app import db
from pytz import timezone
from datetime import datetime

def to_iso(date):
    try:
        return date.isoformat()
    except AttributeError:
        return None

class TipoPedido(db.Model):
    __tablename__ = 'par_tipoPedido'
    pedi_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    pedi_nombre = db.Column(db.String(100), nullable = False)
    

    def __init__(self, pedi_nombre):
        self.pedi_nombre = pedi_nombre

    def __repr__(self):
    
        texto = '''<pedi_id: {}>
        <pedi_nombre: {}>
   '''
        return texto.format(self.pedi_id, self.pedi_nombre)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': int(self.pedi_id),
        'nombre': self.pedi_nombre,
       }




