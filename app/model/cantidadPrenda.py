from app import db

class CantidadPrenda(db.Model):
    __tablename__ = 'par_tcantidadprenda'
    cantidadPrenda_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    cantidadPrenda_nombre_talla_color = db.Column(db.String(50))
    cantidadPrenda_cantidad = db.Column(db.String(50))
    cantidadPrenda_descripcion = db.Column(db.String(700))
    cantidadPrenda_Accesorios = db.Column(db.String(500))
    cantidadPrenda_ValorReferencia  = db.Column(db.Integer)

    def __init__(self, cantidadPrenda_nombre_talla_color, cantidadPrenda_cantidad, cantidadPrenda_descripcion, cantidadPrenda_Accesorios, cantidadPrenda_ValorReferencia):
        self.cantidadPrenda_nombre_talla_color = cantidadPrenda_nombre_talla_color
        self.cantidadPrenda_cantidad = cantidadPrenda_cantidad
        self.cantidadPrenda_descripcion = cantidadPrenda_descripcion
        self.cantidadPrenda_Accesorios = cantidadPrenda_Accesorios
        self.cantidadPrenda_ValorReferencia = cantidadPrenda_ValorReferencia

    def __repr__(self):
        texto = '''<cantidadPrenda_id: {} >
        <cantidadPrenda_nombre_talla_color: {} >
        <cantidadPrenda_cantidad: {} >
        <cantidadPrenda_descripcion: {} >
        <cantidadPrenda_Accesorios: {} >
        <cantidadPrenda_ValorReferencia: {} >
        '''
        return texto.format(self.cantidadPrenda_id ,self.cantidadPrenda_nombre_talla_color, self.cantidadPrenda_cantidad, self.cantidadPrenda_descripcion, self.cantidadPrenda_Accesorios, self.cantidadPrenda_ValorReferencia)