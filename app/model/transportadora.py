from app import db

def to_iso(date):
    try:
        return date.isoformat()
    except AttributeError:
        return None

class Transportadora(db.Model):
    __tablename__ = 'neg_ttransportadora'
    tra_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    tra_encargado = db.Column(db.String(50))
    tra_cedula = db.Column(db.String(12))
    tra_municipio = db.Column(db.Integer)
    tra_barrio = db.Column(db.String(50))
    tra_direccion = db.Column(db.String(100))
    tra_indicaciones = db.Column(db.String(200))
    tra_telefono = db.Column(db.String(50))
    tra_empresa = db.Column(db.String(50))
    tra_emp_telefono = db.Column(db.String(50))
    tra_taquilla = db.Column(db.String(12))
    tra_emp_info = db.Column(db.String(200))
    tra_nombre = db.Column(db.String(50))
    tra_celular = db.Column(db.String(50))
    tra_hora = db.Column(db.Time)
    tra_enc_costos = db.Column(db.String(50))

    def __init__(self, tra_encargado, tra_cedula, tra_municipio, tra_barrio, tra_direccion, tra_indicaciones, tra_telefono, tra_empresa, tra_emp_telefono, tra_taquilla, tra_emp_info, tra_nombre, tra_celular, tra_hora, tra_enc_costos): 
        self.tra_encargado = tra_encargado
        self.tra_cedula = tra_cedula
        self.tra_municipio = tra_municipio
        self.tra_barrio = tra_barrio
        self.tra_direccion = tra_direccion
        self.tra_indicaciones = tra_indicaciones
        self.tra_telefono = tra_telefono
        self.tra_empresa = tra_empresa
        self.tra_emp_telefono = tra_emp_telefono
        self.tra_taquilla = tra_taquilla
        self.tra_emp_info = tra_emp_info
        self.tra_nombre = tra_nombre
        self.tra_celular = tra_celular
        self.tra_hora = tra_hora
        self.tra_enc_costos = tra_enc_costos

    def __repr__(self):
        texto = '''<tra_id: {}>
                   <tra_encargado: {}>
                   <tra_cedula: {}>
                   <tra_municipio: {}>
                   <tra_barrio: {}>
                   <tra_direccion: {}>
                   <tra_indicaciones: {}>
                   <tra_telefono: {}>
                   <tra_empresa: {}>
                   <tra_emp_telefono: {}>
                   <tra_taquilla: {}>
                   <tra_emp_info: {}>
                   <tra_nombre: {}>
                   <tra_celular: {}>
                   <tra_hora: {}>'''
        return texto.format(self.tra_id, self.tra_encargado, self.tra_cedula, self.tra_municipio, self.tra_barrio, self.tra_direccion, self.tra_indicaciones, self.tra_telefono, self.tra_empresa, self.tra_emp_telefono, self.tra_taquilla, self.tra_emp_info, self.tra_nombre, self.tra_celular, self.tra_hora)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': self.tra_id,
        'encargado': self.tra_encargado,
        'cedula': self.tra_cedula,
        'municipio': self.tra_municipio,
        'barrio': self.tra_barrio,
        'direccion': self.tra_direccion,
        'indicaciones': self.tra_indicaciones,
        'telefono': self.tra_telefono,
        'empresa': self.tra_empresa,
        'emp_telefono': self.tra_emp_telefono,
        'taquilla': self.tra_taquilla,
        'emp_info': self.tra_emp_info,
        'nombre': self.tra_nombre,
        'celular': self.tra_celular,
        'hora': to_iso(self.tra_hora),
        'enc_costos': self.tra_enc_costos
       }



