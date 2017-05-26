from app import db

class CantidadPrenda(db.Model):
    __tablename__ = 'par_tReservasPrenda'
    ReservasPrenda_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    ReservasPrenda_nombre = db.Column(db.String(50))
    ReservasPrenda_talla = db.Column(db.String(50))
    ReservasPrenda_color = db.Column(db.String(50))
    ReservasPrenda_entrega = db.Column(db.Datetime)
    ReservasPrenda_devolucion = db.Column(db.Datetime)

    def __init__(self, ReservasPrenda_nombre, ReservasPrenda_talla, ReservasPrenda_color, ReservasPrenda_entrega, ReservasPrenda_devolucion):
        self.ReservasPrenda_nombre = ReservasPrenda_nombre
        self.ReservasPrenda_talla = ReservasPrenda_talla
        self.ReservasPrenda_color = ReservasPrenda_color
        self.ReservasPrenda_entrega = ReservasPrenda_entrega
        self.ReservasPrenda_devolucion = ReservasPrenda_devolucion

    def __repr__(self):
        texto = '''<ReservasPrenda_nombre: {} >
        <ReservasPrenda_talla: {} >
        <ReservasPrenda_color: {} >
        <ReservasPrenda_entrega: {} >
        <ReservasPrenda_devolucion: {} >
        '''
        return texto.format(self.ReservasPrenda_nombre, self.ReservasPrenda_talla, self.ReservasPrenda_color, self.ReservasPrenda_entrega, self.ReservasPrenda_devolucion)