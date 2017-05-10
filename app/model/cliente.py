from app import db
from pytz import timezone
from datetime import datetime

def to_iso(date):
    try:
        return date.isoformat()
    except AttributeError:
        return None

class Cliente(db.Model):
    __tablename__ = 'gen_tcliente'
    cli_identificacion = db.Column(db.DECIMAL, primary_key = True, autoincrement=False)
    cli_nombre = db.Column(db.String(200), nullable = False)
    cli_ciudad = db.Column(db.Integer, nullable = False)
    cli_direccion = db.Column(db.String(200))  
    cli_email = db.Column(db.String(10), nullable = False)
    cli_celular = db.Column(db.String(45), nullable = False)
    cli_telefono = db.Column(db.String(45))
    cli_extension = db.Column(db.String(10))
    cli_cargo = db.Column(db.Integer)
    cli_barrio = db.Column(db.String(100))
    cli_medioConocio = db.Column(db.Integer)
    cli_crea = db.Column(db.String(10))
    cli_modifica = db.Column(db.String(10))
    cli_fecha_mod = db.Column(db.DateTime)
    cli_nacido_mes = db.Column(db.Integer)
    cli_nacido_dia = db.Column(db.Integer)


    def __init__(self, cli_identificacion, cli_nombre, cli_ciudad, cli_direccion,  cli_email, cli_celular, cli_telefono, cli_extension,  cli_barrio, cli_medioConocio, cli_nacido_mes, cli_nacido_dia):
        self.cli_identificacion = cli_identificacion 
        self.cli_nombre = cli_nombre
        self.cli_ciudad = cli_ciudad
        self.cli_direccion = cli_direccion
        self.cli_email = cli_email
        self.cli_celular = cli_celular
        self.cli_telefono = cli_telefono
        self.cli_extension = cli_extension
        self.cli_barrio = cli_barrio
        self.cli_medioConocio = cli_medioConocio
        self.cli_fecha_mod = datetime.now(timezone('America/Bogota'))
        self.cli_nacido_mes = cli_nacido_mes
        self.cli_nacido_dia = cli_nacido_dia


    def __repr__(self):
    
        texto = '''<cli_nombre: {}>
        <cli_apellido: {}>
        <cli_ciudad: {}>
        <cli_direccion: {}>
        <cli_email: {}>
        <cli_celular: {}>
        <cli_telefono: {}>
        <cli_extension: {}>
        <cli_cargo: {}>
        <cli_barrio: {}>
        <cli_medioConocio: {}>
        <cli_crea: {}>
        <cli_modifica: {}>
        <cli_nacido_mes: {}>
        <cli_nacido_dia: {}>'''
        return texto.format(self.cli_nombre, self.cli_apellido, self.cli_ciudad, self.cli_direccion,  self.cli_email, self.cli_celular, self.cli_telefono, self.cli_extension, self.cli_cargo, self.cli_barrio, self.i_medioConocio, self.cli_crea, self.cli_modifica,self.cli_nacido_mes, self.cli_nacido_dia)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'identificacion': int(self.cli_identificacion),
        'nombre': self.cli_nombre,
        'apellido': self.cli_apellido,
        'ciudad': self.cli_ciudad,
        'direccion': self.cli_direccion,
        'email': self.cli_email,
        'celular': self.cli_celular,
        'telefono': self.cli_telefono,
        'extension': self.cli_extension,
        'cargo': self.cli_cargo,
        'barrio': self.cli_barrio,
        'medioConocio': self.cli_medioConocio,
        'crea': self.cli_crea,
        'modifica': self.cli_modifica,
        'fecha_mod': to_iso(self.cli_fecha_mod),
        'nacido_mes': self.cli_nacido_mes,
        'nacido_dia': self.cli_nacido_dia,
       }




