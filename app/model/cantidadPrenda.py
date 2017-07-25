from app import db

class CantidadPrenda(db.Model):
    __tablename__ = 'par_tcantidadprenda'
    cantidadPrenda_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    cantidadPrenda_nombre_talla_color = db.Column(db.String(50))
    cantidadPrenda_cantidad = db.Column(db.String(50))
    cantidadPrenda_descripcion = db.Column(db.String(700))
    cantidadPrenda_Accesorios = db.Column(db.String(500))
    cantidadPrenda_ValorReferencia  = db.Column(db.Integer)
    SexoLinea = db.Column(db.String(100))
    Estilo =  db.Column(db.String(200))

    def __init__(self, cantidadPrenda_nombre_talla_color, cantidadPrenda_cantidad, cantidadPrenda_descripcion, cantidadPrenda_Accesorios, cantidadPrenda_ValorReferencia,SexoLinea,Estilo):
        self.cantidadPrenda_nombre_talla_color = cantidadPrenda_nombre_talla_color
        self.cantidadPrenda_cantidad = cantidadPrenda_cantidad
        self.cantidadPrenda_descripcion = cantidadPrenda_descripcion
        self.cantidadPrenda_Accesorios = cantidadPrenda_Accesorios
        self.cantidadPrenda_ValorReferencia = cantidadPrenda_ValorReferencia
        self.SexoLinea = SexoLinea
        self.Estilo = Estilo 

    def __repr__(self):
        texto = '''<cantidadPrenda_id: {} >
        <cantidadPrenda_nombre_talla_color: {} >
        <cantidadPrenda_cantidad: {} >
        <cantidadPrenda_descripcion: {} >
        <cantidadPrenda_Accesorios: {} >
        <cantidadPrenda_ValorReferencia: {} >
        <SexoLinea: {} >
        <Estilo: {} >
        '''
        return texto.format(self.cantidadPrenda_id ,self.cantidadPrenda_nombre_talla_color, self.cantidadPrenda_cantidad, self.cantidadPrenda_descripcion, self.cantidadPrenda_Accesorios, self.cantidadPrenda_ValorReferencia,self.SexoLinea, self.Estilo)