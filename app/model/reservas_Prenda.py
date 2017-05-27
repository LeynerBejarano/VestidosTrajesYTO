from app import db

class CantidadPrenda(db.Model):
    __tablename__ = 'par_tReservasPrenda'
    ReservasPrenda_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    cantidadPrenda_nombre_talla_color = db.Column(db.String(200))
    ReservasPrenda_entrega = db.Column(db.Datetime)
    ReservasPrenda_devolucion = db.Column(db.Datetime)

    def __init__(self, cantidadPrenda_nombre_talla_color ReservasPrenda_entrega, ReservasPrenda_devolucion):
        self.cantidadPrenda_nombre_talla_color = cantidadPrenda_nombre_talla_color
        self.ReservasPrenda_entrega = ReservasPrenda_entrega
        self.ReservasPrenda_devolucion = ReservasPrenda_devolucion

    def __repr__(self):
        texto = '''<cantidadPrenda_nombre_talla_color: {} >

        <ReservasPrenda_entrega: {} >
        <ReservasPrenda_devolucion: {} >
        '''
        return texto.format(self.cantidadPrenda_nombre_talla_color self.ReservasPrenda_entrega, self.ReservasPrenda_devolucion)