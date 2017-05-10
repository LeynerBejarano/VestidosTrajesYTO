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
from flask import render_template, redirect, request, jsonify, url_for, flash,send_from_directory, Flask
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


@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    datos = {'title' : 'Facturación ikotia'}

    ##### Cargado de datos desde la base de datos.
    cargos = Cargo.query.order_by(Cargo.crg_descripcion)
    ciudades = Ciudad.query.order_by(Ciudad.ciu_nombre)
    eventos = Evento.query.order_by(Evento.eve_id)
    jornadas = Jornada.query.order_by(Jornada.jor_id)
    niveles = Nivele.query.order_by(Nivele.niv_id)
    clases = Clase.query.order_by(Clase.cla_id)
    tallas = Talla.query.order_by(Talla.tal_id)
    tipos = Tipo.query.order_by(Tipo.tip_nombre)
    presindivs = Presindiv.query.order_by(Presindiv.pri_nombre)
    prespedidos = Prespedido.query.order_by(Prespedido.prp_nombre)
    prestamos = Prestamo.query.order_by(Prestamo.prs_nombre)
    tipos_est = Tipo_estola.query.order_by(Tipo_estola.tes_id)
    presentaciones = Presentacion.query.order_by(Presentacion.prs_nombre)
    terminaciones = Terminacion.query.order_by(Terminacion.ter_nombre)
    entregas = Entrega.query.order_by(Entrega.ent_id)
    estados_fin = Estado_fin.query.order_by(Estado_fin.esf_nombre)
    estados_com = Estado_com.query.order_by(Estado_com.esc_nombre)
    estados = Estado.query.order_by(Estado.esp_nombre)
    vendedores = Usuario.query.filter(Usuario.usu_rol.like('%vendedor%')).order_by(Usuario.usu_nombre)
    tipos_orden = Tipo_orden.query.order_by(Tipo_orden.tip_id)
    medioConocio = MedioConocio.query.order_by(MedioConocio.medio_id)
    tipoPedido = TipoPedido.query.order_by(TipoPedido.pedi_id)



    #### Creacion de arreglos usados en el auto-completar de jquery
    cedulas = []
    for cli in Cliente.query:
      cedulas.append(int(cli.cli_identificacion))

    form = Form_Pedido()

    #### Agregar entradas a los FieldList solo cuando se carga la pagina, para evitar datos duplicados en la validacion

    
        

    ### Volcado de datos en el fieldlist Detalles

    

      

      ###Estilos
      



    ### Volcado de datos en otros selectores/Radio buttons del formulario
    choices = [(ti.pedi_id, ti.pedi_nombre) for ti in tipoPedido or []] + [(-1, 'Otro')]
    form.fac_tipoPedido.choices = choices
    choices = [(m.medio_id, m.medio_nombre) for m in medioConocio or []] + [(-1, 'Otro')]
    form.cli_medioConocio.choices = choices
    choices = [(c.ciu_id, c.ciu_nombre) for c in ciudades or []] + [(-1, 'Otro')]
    form.municipio_enc.choices = choices
    form.ins_ciudad.choices = choices
    choices = [(e.eve_id, e.eve_nombre) for e in eventos or []] + [(-1, 'Otro')]
    form.ped_evento.choices = choices
    choices = [(t.tip_id, t.tip_nombre) for t in tipos_orden or []]
    form.ent_tipo_orden.choices = choices
    form.rec_tipo_orden.choices = choices
    form.tipo_entrega_ord.choices = choices
    form.tipo_recogida_ord.choices = choices

    choices = [(c.cla_id - 1, c.cla_id - 1) for c in clases or []]
    form.principal.choices = choices
    form.dia_enc.choices = [(i, str(i)) for i in range(1,32) or []]
      

    ####### SUBMIT ######
    
    

    return render_template('pedido.html',datos = datos,form = form,clases = clases,tallas = tallas, cedulas = cedulas,cliente = request.args.get('cliente'),pedido = request.args.get('pedido'))

@app.route('/insertarCliente', methods=['GET','POST'])
def insertarCliente():

  nombre = request.form.get('txtNonmbreCliente')#['txtNonmbreCliente']
  CcNit = request.form.get('txtCC_Nit')#['txtCC_Nit']
  DiaCumpleaños = request.form.get('txtDiaCumpleaños')#[]
  MesCumpleaños = request.form.get('txtMesCumpleaños')#[]
  TelFijo = request.form.get('txtTelefonoFijo')#[]
  Ext =  request.form.get('Ext')#[]
  Celular = request.form.get('txtCelular')#[]
  Email = request.form.get('txtEmail')#[]
  Direccion = request.form.get('txtDireccion')#[]
  Municipio = int(request.form.get('txtMunicipio'))#[]
  Barrio = request.form.get('txtBarrio')#[]
  Barrio = request.form.get('txtBarrio')#[]
  ReferenciaNombre = request.form.get('txtReferenciaNombre')#[]
  ReferenciaCelular = request.form.get('txtReferenciaCelular')#[]
  ReferenciaTelefono = request.form.get('txtReferenciaTElefono')#[]
  cliMedio= 3
  new_cli = Cliente(123456789012, 'nombre', 1, 'Direccion', 'Email', 'Celular', 'TelFijo','Ext', 'Barrio', 3, 'MesCumpleaños', 'DiaCumpleaños')
  db.session.add(new_cli)
  db.session.commit()
  return jsonify({'nombre': nombre})
  return jsonify({'error': 'Missing data'})

  

 


  
                        


                        
                         
                         
                         
