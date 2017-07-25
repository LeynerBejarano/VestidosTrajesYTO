from app import db

class HoraRecogidaReserva(db.Model):
    __tablename__ = 'neg_horarecogidareserva'
    HoraReco_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    HoraReco_fechaSlash = db.Column(db.DateTime)
    HoraReco_fechaGuion  = db.Column(db.String(80))
    HoraReco_hora = db.Column(db.Integer)
   

    def __init__(self,  HoraReco_fechaSlash, HoraReco_fechaGuion,  HoraReco_hora):
        self.HoraReco_fechaSlash = HoraReco_fechaSlash
        self.HoraReco_fechaGuion = HoraReco_fechaGuion
        self.HoraReco_hora       = HoraReco_hora
        

    def __repr__(self):
        texto = '''<HoraReco_fechaSlash: {} >
        <HoraReco_fechaGuion: {} >
        <HoraReco_hora      : {} >
        '''
        return texto.format(self.HoraReco_fechaSlash,self.HoraReco_fechaGuion,self.HoraReco_hora)