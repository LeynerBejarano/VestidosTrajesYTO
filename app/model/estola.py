from app import db

class Estola(db.Model):
    __tablename__ = 'neg_testola'
    etl_estola = db.Column(db.Integer, primary_key = True, autoincrement=True)
    etl_tamano = db.Column(db.Integer)
    etl_doble_faz = db.Column(db.Integer)
    etl_flequillo = db.Column(db.Integer)
    etl_terminacion = db.Column(db.Integer)
    etl_presentacion = db.Column(db.Integer)


    def __init__(self, etl_estola, etl_tamano, etl_doble_faz, etl_flequillo, etl_terminacion, etl_presentacion):
        self.etl_estola = etl_estola
        self.etl_tamano = etl_tamano
        self.etl_doble_faz = etl_doble_faz
        self.etl_flequillo = etl_flequillo
        self.etl_terminacion = etl_terminacion
        self.etl_presentacion = etl_presentacion

    def __repr__(self):
        texto = '''<etl_estola: {} >'''
        return texto.format(self.etl_estola)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'estola': self.etl_estola,
        'tamano': self.etl_tamano,
        'doble_faz': self.etl_doble_faz,
        'flequillo': self.etl_flequillo,
        'terminacion': self.etl_terminacion,
        'presentacion': self.etl_presentacion
       }
