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

class PassSkill(db.Model):
    __tablename__ = 'gen_passskill'
    PassSKill_id  =  db.Column(db.Integer, primary_key = True, autoincrement=True)
    PassSKill_skill = db.Column(db.String(200))
    PassSKill_text  = db.Column(db.String(200))

    

    

    def __init__(self,PassSKill_skill,PassSKill_text):  
        self.PassSKill_skill= PassSKill_skill
        self.PassSKill_text = PassSKill_text 
        
       


    def __repr__(self):
        texto = '''<PassSKill_id   : {}> 
        <PassSKill_skill : {}>
        <PassSKill_text  : {}>
               '''
        return texto.format(self.PassSKill_id, self.PassSKill_skill,self.PassSKill_text)
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       'id': self.PassSKill_id,
        'skill': self.PassSKill_skill,
        'text': self.PassSKill_text
       }
       


