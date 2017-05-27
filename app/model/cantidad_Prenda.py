from app import db

class CantidadPrenda(db.Model):
    __tablename__ = 'par_tcantidadPrenda'
    cantidadPrenda_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    cantidadPrenda_nombre_talla_color = db.Column(db.String(50))
    cantidadPrenda_cantidad = db.Column(db.String(50))

    def __init__(self, cantidadPrenda_nombre_talla_color, cantidadPrenda_cantidad):
        self.cantidadPrenda_nombre_talla_color = cantidadPrenda_nombre_talla_color
        self.cantidadPrenda_cantidad = cantidadPrenda_cantidad

    def __repr__(self):
        texto = '''<cantidadPrenda_nombre_talla_color: {} >
        <cantidadPrenda_cantidad: {} >
        '''
        return texto.format(self.cantidadPrenda_nombre_talla_color, self.cantidadPrenda_cantidad)