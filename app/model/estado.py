from app import db

class Estado(db.Model):
    __tablename__ = 'par_testado_ped'
    esp_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    esp_nombre = db.Column(db.String, nullable = False)

    def __init__(self, esp_nombre):
        self.esp_nombre = esp_nombre

    def __repr__(self):
        texto = '''<esp_nombre: {} >'''
        return texto.format(self.esp_nombre)