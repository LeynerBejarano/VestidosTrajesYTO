import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.principal import Principal, Permission, RoleNeed
from flask.ext.mail import Mail
from config import basedir
from sqlalchemy import *

####PDF library-> pip3 install --pre xhtml2pdf


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()

principals = Principal(app)
# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))

lm.init_app(app)
lm.login_view = 'login'

mail_ext = Mail(app)

from app import login, prendas, pedido, accesorios, cliente, prospectos, buscar, municipio, excel, abonos
from app.model import user
from app.model import prenda
from app.model import color


