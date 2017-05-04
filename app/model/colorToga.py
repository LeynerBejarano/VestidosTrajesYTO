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

class ColorToga(db.Model):
    __tablename__ = 'par_tcolorToga'
    colorToga_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    colorToga_nombre = db.Column(db.Integer, nullable = False)
  
    

    def __init__(self, colorToga_id, colorToga_nombre,):
        self.colorToga_id = colorToga_id
        self.colorToga_nombre = colorToga_nombre
        
       


    def __repr__(self):
        texto = '''<colorToga_id: {}>
        <colorToga_nombre: {}>
               '''
        return texto.format(self.colorToga_id, self.colorToga_nombre)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'colorToga_id': self.colorToga_id,
        'colorToga_nombre': self.colorToga_nombre,
       }
       


