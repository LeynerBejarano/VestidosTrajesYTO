from app import db

class CantidadPrenda(db.Model):
    __tablename__ = 'par_tcantidadPrenda'
    cantidadPrenda_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    cantidadPrenda_nombre = db.Column(db.String(50))
    cantidadPrenda_talla = db.Column(db.String(50))
    cantidadPrenda_color = db.Column(db.String(50))
    cantidadPrenda_cantidad = db.Column(db.String(50))

    def __init__(self, cantidadPrenda_nombre, cantidadPrenda_talla, cantidadPrenda_color, cantidadPrenda_cantidad):
        self.cantidadPrenda_nombre = cantidadPrenda_nombre
        self.cantidadPrenda_talla = cantidadPrenda_talla
        self.cantidadPrenda_color = cantidadPrenda_color
        self.cantidadPrenda_cantidad = cantidadPrenda_cantidad

    def __repr__(self):
        texto = '''<cantidadPrenda_nombre: {} >
        <cantidadPrenda_talla: {} >
        <cantidadPrenda_color: {} >
        <cantidadPrenda_cantidad: {} >
        '''
        return texto.format(self.cantidadPrenda_nombre, self.cantidadPrenda_talla, self.cantidadPrenda_color, self.cantidadPrenda_cantidad)