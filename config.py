import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'wacor-is-a-god'

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = basedir + '/uploads/'
#'mysql+pymysql://losdelastogas:togas2016@losdelastogas.mysql.pythonanywhere-services.com/losdelastogas$ikotia'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/luifer'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True


##### Email settings
DEBUG=True
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
# MAIL_USERNAME = '.@cidenet.org'
# MAIL_PASSWORD = ''
MAIL_USERNAME = 'losdelastogas@gmail.com'
MAIL_PASSWORD = '101116togas'

