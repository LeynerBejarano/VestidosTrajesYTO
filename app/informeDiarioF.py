import os
from flask import render_template, redirect, request, jsonify, send_from_directory, flash, url_for
from flask.ext.wtf import Form
from wtforms import StringField, DecimalField, SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import IntegerField
from werkzeug import secure_filename
from wtforms.validators import DataRequired, Optional
from app import app, db
from flask.ext.login import login_required, current_user
from app.model.cliente import Cliente
from app.model.cargo import Cargo
from flask.ext.login import current_user
from app.model.ciudad import Ciudad
from pytz import timezone
from datetime import datetime



class Employee:
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, salary):
      self.FacturaNo = FacturaNo
      self.FacturaValor = FacturaValor
      self.ReciboNo = ReciboNo
      self.ReciboNoFactura = ReciboNoFactura
      self.ReciboValor = ReciboValor
      self.ReciboConcepto = ReciboConcepto
      self.Ingreso = Ingreso
      self.Egreso = Egreso
      self.Saldo = Saldo 
      



