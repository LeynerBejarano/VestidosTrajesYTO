from app import db
 
class Recurso(db.Model):
    __tablename__ = 'gen_trecurso'
    rec_id = db.Column(db.Integer, primary_key = True)
    rec_url = db.Column(db.String(255))

    # Codigo del recurso
    @property
    def rec_id(self):
        return self.rec_id

    @rec_id.setter
    def rec_id(self, recurso):
        self.rec_id = recurso

    # URL del recurso
    @property
    def rec_url(self):
        return self.rec_url

    @rec_url.setter
    def rec_url(self, url):
        self.rec_url = url

    # Representación en texto del objeto
    def __repr__(self):
        texto = '''<Código: {} >
                <URL: {} >'''
        return texto.format(self.rec_id, self.rec_url)