from app import db

class Det_estola(db.Model):
    __tablename__ = 'neg_tdet_estola'
    etl_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    etl_imagen = db.Column(db.String(50))
    etl_detalle = db.Column(db.Integer)
    etl_tipo = db.Column(db.Integer)
    etl_tipo_escudo = db.Column(db.Integer)
    etl_tamano = db.Column(db.Integer)
    etl_doble_faz = db.Column(db.Integer)
    etl_flequillo = db.Column(db.Integer)
    etl_personalizada = db.Column(db.Integer)
    etl_terminacion = db.Column(db.Integer)
    etl_presentacion = db.Column(db.Integer)
    etl_lado_izq = db.Column(db.String(200))
    etl_lado_der = db.Column(db.String(200))
    etl_sesgo = db.Column(db.Integer)
    etl_sesgo_color = db.Column(db.Integer)


    def __init__(self, etl_imagen, etl_detalle, etl_tipo, etl_tipo_escudo, etl_tamano, etl_doble_faz, etl_flequillo, etl_personalizada, etl_terminacion, etl_presentacion, etl_lado_izq, etl_lado_der, etl_sesgo, etl_sesgo_color):
        self.etl_imagen = etl_imagen
        self.etl_detalle = etl_detalle
        self.etl_tipo = etl_tipo
        self.etl_tipo_escudo = etl_tipo_escudo
        self.etl_tamano = etl_tamano
        self.etl_doble_faz = etl_doble_faz
        self.etl_flequillo = etl_flequillo
        self.etl_personalizada = etl_personalizada
        self.etl_terminacion = etl_terminacion
        self.etl_presentacion = etl_presentacion
        self.etl_lado_izq = etl_lado_izq
        self.etl_lado_der = etl_lado_der
        self.etl_sesgo = etl_sesgo
        self.etl_sesgo_color = etl_sesgo_color

    def __repr__(self):
        texto = '''<etl_imagen: {} >'''
        return texto.format(self.etl_imagen)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
        'id': self.etl_id,
        'imagen': self.etl_imagen,
        'detalle': self.etl_detalle,
        'tipo': self.etl_tipo,
        'tipo_escudo': self.etl_tipo_escudo,
        'tamano': self.etl_tamano,
        'doble_faz': self.etl_doble_faz,
        'flequillo': self.etl_flequillo,
        'terminacion': self.etl_terminacion,
        'presentacion': self.etl_presentacion,
        'personalizada': self.etl_personalizada,
        'lado_izq': self.etl_lado_izq,
        'lado_der': self.etl_lado_der,
        'sesgo': self.etl_sesgo,
        'sesgo_color': self.etl_sesgo_color
       }
