import os
from app import app, db, mail_ext, admin_permission
from datetime import datetime, timedelta, date
from pytz import timezone
from calendar import monthrange, month_name
from zipfile import ZipFile
from werkzeug import secure_filename
from xhtml2pdf import pisa
from io import BytesIO
from sqlalchemy.sql import func
from flask.ext.login import login_required, current_user
from flask_wtf.file import FileField
from flask import render_template, redirect, request, jsonify, url_for, flash,send_from_directory
from flask.ext.mail import Mail, Message
from flask.ext.principal import Identity
from .form_pedido import Form_Pedido
from app.model.cargo import Cargo
from app.model.ciudad import Ciudad
from app.model.evento import Evento
from app.model.jornada import Jornada
from app.model.nivele import Nivele
from app.model.prenda import Prenda
from app.model.color import Color
from app.model.estilo import Estilo
from app.model.accesorio import Accesorio
from app.model.cliente import Cliente
from app.model.empresa import Empresa
from app.model.user import Usuario
from app.model.institucion import Institucion
from app.model.pedido import Pedido
from app.model.det_pedido import Det_pedido
from app.model.prospecto import Prospecto
from app.model.det_prospecto import Det_prospecto
from app.model.clase import Clase
from app.model.presindiv import Presindiv
from app.model.prespedido import Prespedido
from app.model.prestamo import Prestamo
from app.model.despacho import Despacho
from app.model.det_despacho import Det_despacho
from app.model.det_estola import Det_estola
from app.model.pro_estola import Pro_estola
from app.model.tipo import Tipo
from app.model.talla import Talla
from app.model.entrega import Entrega
from app.model.tipo_estola import Tipo_estola
from app.model.terminacion import Terminacion
from app.model.presentacion import Presentacion
from app.model.estado_com import Estado_com
from app.model.estado_fin import Estado_fin
from app.model.estado import Estado
from app.model.orden import Orden
from app.model.personalizada import Personalizada
from app.model.transportadora import Transportadora
from app.model.tipo_orden import Tipo_orden
from app.model.medioConocio import MedioConocio
from app.model.tipoPedido import TipoPedido
from app.utils import numero_a_letras, timeRange, get_temporada, text_to_time


@app.route('/insertarCliente', methods=['GET','POST'])
def insertarCliente():

  nombre = request.form['txtNonmbreCliente']
  CcNit = request.form['txtCC/Nit']
  DiaCumpleaños = request.form['txtDiaCumpleaños']
  MesCumpleaños = request.form['txtMesCumpleaños']
  TelFijo = request.form['txtTelefonoFijo']
  Ext =  request.form['Ext.']
  Celular = request.form['txtCelular']
  Email = request.form['txtEmail']
  Direccion = request.form['txtDireccion']
  Municipio = request.form['txtMunicipio']
  Barrio = request.form['txtBarrio']
  Barrio = request.form['txtBarrio']
  ReferenciaNombre = request.form['txtReferenciaNombre']
  ReferenciaCelular = request.form['txtReferenciaCelular']
  ReferenciaTelefono = request.form['txtReferenciaTElefono']
  cliMedio= 3
  if nombre is not none:
    new_cli = Cliente(CcNit, nombre, Municipio, Direccion, Email, Celular, TelFijo, Barrio, cliMedio, MesCumpleaños, DiaCumpleaños)
    db.session.add(new_cli)
    db.session.commit()
    return jsonify({'nombre': nombre})
    return jsonify({'error': 'Missing data'})

  return render_template('pedido.html',datos = datos,form = form,clases = clases,tallas = tallas, cedulas = cedulas,cliente = request.args.get('cliente'),pedido = request.args.get('pedido'))

               
              
    

  
  
  #return redirect('/pedidos')
