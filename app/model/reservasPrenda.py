from app import db

class ReservasPrenda(db.Model):
    __tablename__ = 'neg_treservasprenda'
    ReservasPrenda_id = db.Column(db.Integer, primary_key = True, autoincrement=False)
    ReservasPrenda_Cantidad = db.Column(db.Integer)
    ReservasPrenda_entrega_nombre_talla_color = db.Column(db.Integer)
    DiaRecoger = db.Column(db.Integer)
    MesRecoger = db.Column(db.Integer)
    AñoRecoger = db.Column(db.Integer)
    ReservasPrenda_entrega = db.Column(db.DateTime)
    DiaEntregar = db.Column(db.Integer)
    MesEntregar = db.Column(db.Integer)
    AñoEntregar = db.Column(db.Integer)
    ReservasPrenda_devolucion = db.Column(db.DateTime)

    def __init__(self, ReservasPrenda_Cantidad, ReservasPrenda_entrega_nombre_talla_color, DiaRecoger, MesRecoger, AñoRecoger, ReservasPrenda_entrega, DiaEntregar, MesEntregar, AñoEntregar, ReservasPrenda_devolucion):
        self.ReservasPrenda_Cantidad = ReservasPrenda_Cantidad
        self.ReservasPrenda_entrega_nombre_talla_color = ReservasPrenda_entrega_nombre_talla_color
        self.DiaRecoger = DiaRecoger
        self.MesRecoger = MesRecoger 
        self.AñoRecoger = AñoRecoger
        self.ReservasPrenda_entrega = ReservasPrenda_entrega
        self.DiaEntregar = DiaEntregar 
        self.MesEntregar = MesEntregar 
        self.AñoEntregar = AñoEntregar
        self.ReservasPrenda_devolucion = ReservasPrenda_devolucion

    def __repr__(self):
        texto = '''<ReservasPrenda_Cantidad: {} >
        <ReservasPrenda_entrega_nombre_talla_color: {} >
        <DiaRecoger: {}> 
        <MesRecoger: {}> 
        <AñoRecoger: {}> 
        <ReservasPrenda_entrega: {} >
        <DiaEntregar: {}>
        <MesEntregar: {}>
        <AñoEntregar: {}>
        <ReservasPrenda_devolucion: {} >
        '''
        return texto.format(self.ReservasPrenda_Cantidad ,self.ReservasPrenda_entrega_nombre_talla_color, self.DiaRecoger, self.MesRecoger,self.AñoRecoger, self.ReservasPrenda_entrega, self.DiaEntregar, self.MesEntregar, self.AñoEntregar, self.ReservasPrenda_devolucion)