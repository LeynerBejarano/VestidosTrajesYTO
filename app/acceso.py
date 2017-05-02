from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
 
class Login(Form):
    usuario = StringField('usuario', validators=[DataRequired()])
    clave = PasswordField('clave', validators=[DataRequired()])
    recordarme = BooleanField('recordarme', default=False)