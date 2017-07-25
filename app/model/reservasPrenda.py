from app import db

class ReservasPrenda(db.Model):
    __tablename__ = 'neg_treservasprenda'
    ReservasPrenda_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    ReservasPrenda_entrega_nombre_talla_color = db.Column(db.Integer)
    ReservasPrenda_entrega = db.Column(db.DateTime)
    ReservasPrenda_devolucion = db.Column(db.DateTime)
    ReservasPrenda_factura = db.Column(db.Integer)

    def __init__(self,  ReservasPrenda_entrega_nombre_talla_color, ReservasPrenda_entrega,  ReservasPrenda_devolucion, ReservasPrenda_factura):
        self.ReservasPrenda_entrega_nombre_talla_color = ReservasPrenda_entrega_nombre_talla_color
        self.ReservasPrenda_entrega = ReservasPrenda_entrega
        self.ReservasPrenda_devolucion = ReservasPrenda_devolucion
        self.ReservasPrenda_factura = ReservasPrenda_factura

    def __repr__(self):
        texto = '''<ReservasPrenda_entrega_nombre_talla_color: {} > 
        <ReservasPrenda_entrega: {} >
        <ReservasPrenda_devolucion: {} >
        <ReservasPrenda_factura: {} >
        '''
        return texto.format(self.ReservasPrenda_entrega_nombre_talla_color,  self.ReservasPrenda_entrega,  self.ReservasPrenda_devolucion, self.ReservasPrenda_factura)