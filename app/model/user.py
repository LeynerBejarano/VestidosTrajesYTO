from werkzeug.security import generate_password_hash, check_password_hash
from app import db
 
class Usuario(db.Model):
    __tablename__ = 'sec_tusuario'
    usu_login = db.Column(db.String(10), primary_key = True)
    usu_password = db.Column(db.String(50), nullable = False)
    usu_nombre = db.Column(db.String(200), nullable = False)
    usu_apellido = db.Column(db.String(200), nullable = False)
    usu_acceso = db.Column(db.Date)
    usu_permiso = db.Column(db.String(150), nullable = False)
    usu_rol = db.Column(db.String(2))
    usu_empresa = db.Column(db.Integer, nullable = False)
    usu_estado = db.Column(db.Boolean, nullable = False, default = True)
    usu_crea = db.Column(db.String(10))
    usu_modifica = db.Column(db.String(10))
    usu_fecha_mod = db.Column(db.DateTime)
    usu_relacion = db.Column(db.String(45))

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            unicode = str
            text_type = unicode
            return text_type(self.usu_login)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    # Representación en texto del objeto
    def __repr__(self):
        texto = '''<Usuario: {} >
                <Nombre Completo: {} {}>
                <ütimo acceso: {} >
                <Rol: {} >
                <Empresa: {} >
                <Estado: {} >'''
        return texto.format(self.usu_login, self.usu_nombre, self.usu_apellido, 
                            self.usu_acceso, self.usu_rol, self.usu_empresa, 
                            self.usu_estado)