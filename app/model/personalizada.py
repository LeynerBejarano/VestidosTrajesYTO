from app import db
from pytz import timezone
from datetime import datetime

class Personalizada(db.Model):
    __tablename__ = 'neg_tpersonalizada'
    per_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    per_encargado = db.Column(db.String(50))
    per_cedula = db.Column(db.String(20))
    per_celular = db.Column(db.String(50))
    per_direccion = db.Column(db.String(100))
    per_indicaciones = db.Column(db.String(200))
    per_municipio = db.Column(db.Integer)
    per_lugar = db.Column(db.String(20))
    per_barrio = db.Column(db.String(50))
    per_repartidores = db.Column(db.Integer)
    per_cel_repartidor = db.Column(db.String(50))

    def __init__(self, per_encargado, per_cedula, per_celular, per_direccion, per_indicaciones, per_municipio, per_lugar, per_barrio, per_repartidores, per_cel_repartidor): 
        self.per_encargado = per_encargado
        self.per_cedula = per_cedula
        self.per_celular = per_celular
        self.per_direccion = per_direccion
        self.per_indicaciones = per_indicaciones
        self.per_municipio = per_municipio
        self.per_lugar = per_lugar
        self.per_barrio = per_barrio
        self.per_repartidores = per_repartidores
        self.per_cel_repartidor = per_cel_repartidor

    def __repr__(self):
        texto = '''<per_id: {}>
                   <per_encargado: {}>
                   <per_cedula: {}>
                   <per_celular: {}>
                   <per_direccion: {}>
                   <per_indicaciones: {}>
                   <per_municipio: {}>
                   <per_lugar: {}>
                   <per_barrio: {}>
                   <per_repartidores: {}>
                   <per_cel_repartidor: {}>'''
        return texto.format(self.per_id, self.per_encargado, self.per_cedula, self.per_celular, self.per_direccion, self.per_indicaciones, self.per_municipio, self.per_lugar, self.per_barrio, self.per_repartidores, self.per_cel_repartidor)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': self.per_id,
        'encargado': self.per_encargado,
        'cedula': self.per_cedula,
        'celular': self.per_celular,
        'direccion': self.per_direccion,
        'indicaciones': self.per_indicaciones,
        'municipio': self.per_municipio,
        'lugar': self.per_lugar,
        'barrio': self.per_barrio,
        'repartidores': self.per_repartidores,
        'cel_repartidor': self.per_cel_repartidor
       }



