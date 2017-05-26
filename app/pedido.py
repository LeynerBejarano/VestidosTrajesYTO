import os
from app import app, db, mail_ext, admin_permission
from datetime import datetime, timedelta, date
from pytz import timezone
from calendar import monthrange, month_name
from zipfile import ZipFile
from werkzeug import secure_filename
from xhtml2pdf import pisa
from io import BytesIO, StringIO
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
from app.model.factura import Factura
from app.utils import numero_a_letras, timeRange, get_temporada, text_to_time
from pdfkit import api
from flask import make_response
from flask import send_file,Response


#from wkhtmltopdf import WKHtmlToPdf
#from wkhtmltopdf.main import WKhtmlToPdf



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
    choices = [(v.usu_login, v.usu_nombre + ' ' + v.usu_apellido if v.usu_estado == 1 else 'Inactivo - ' + v.usu_nombre + ' ' + v.usu_apellido) for v in vendedores]
    form.vendedor.choices = choices
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

  
  nombre = request.form.get('txtNonmbreCliente')
  
  CcNit = request.form.get("txtCC_Nit")
  DiaCumpleaños = request.form.get("txtDiaCumpleaños")
  MesCumpleaños = request.form.get('txtMesCumpleaños')#[]
  TelFijo = request.form.get("txtTelefonoFijo")
  Ext = request.form.get("Ext")
  Celular = request.form.get("txtCelular")
  Email = request.form.get('txtEmail')#[]
  Direccion = request.form.get('txtDireccion')#[]
  Municipio = request.form.get('txtMunicipio')#[]
  Barrio = request.form.get('txtBarrio')#[]
  MedioConocio = request.form.get('txtMedioConocio')#[]
  Poblacion = request.form.get('txtPedPoblacion')
  #
  #
  #
  TipoPedido = request.form.get('txtTipoPedido')
  TipoEvento = request.form.get('txtTipoEvento')
  DiaEvento = request.form.get('txtDiaEvento')
  MesEvento = request.form.get('txtMesEvento')
  AñoEvento = request.form.get('txtAñoEvento')
  Referencia1 = request.form.get('txtReferencia1')
  Descripcion1 = request.form.get('txtDescripcion1')
  Accesorios1 = request.form.get('txtAccesorios1')
  MedidasArreglos1 = request.form.get('txtMedidasArreglos1')
  ValorReferencia1 = request.form.get('txtValorReferencia1')
  Referencia2 = request.form.get('txtReferencia2')
  Descripcion2 = request.form.get('txtDescripcion2')
  Accesorios2 = request.form.get('txtAccesorios2')
  MedidasArreglos2 = request.form.get('txtMedidasArreglos2')
  ValorReferencia2 = request.form.get('txtValorReferencia2')
  Referencia3 = request.form.get('txtReferencia3')
  Descripcion3 = request.form.get('txtDescripcion3')
  Accesorios3 = request.form.get('txtAccesorios3')
  MedidasArreglos3 = request.form.get('txtMedidasArreglos3')
  ValorReferencia3 = request.form.get('txtValorReferencia3')
  Referencia4 = request.form.get('txtReferencia4')
  Descripcion4 = request.form.get('txtDescripcion4')
  Accesorios4 = request.form.get('txtAccesorios4')
  MedidasArreglos4 = request.form.get('txtMedidasArreglos4')
  ValorReferencia4 = request.form.get('txtValorReferencia4')
  #
  DiaRecoger = request.form.get('txtDiaRecoger')
  MesRecoger = request.form.get('txtMesRecoger')
  AñoRecoger = request.form.get('txtAñoRecoger')
  DiaEntregar = request.form.get('txtDiaEntregar')
  MesEntregar = request.form.get('txtMesEntregar')
  AñoEntregar =  request.form.get('txtAñoEntregar')
  Saldo = request.form.get('txtSaldo')
  Total = request.form.get('txtTotal')
  Abono =  request.form.get('txtAbono')
  Retefuente = request.form.get('txtRetefuente')
  ReferenciaNombre = request.form.get('txtReferenciaNombre')#[]
  ReferenciaCelular = request.form.get('txtReferenciaCelular')#[]
  ReferenciaTelefono = request.form.get('txtReferenciaTelefono')#[]
  Nota = request.form.get('txtNota')#[]
  #
  ConsecutivoManual = request.form.get('txtConsecutivoManual')#[]z
  Consecutivo = request.form.get('txtConsecutivo')#[]z
  if Cliente.query.get(CcNit) is None:
    new_cli = Cliente(CcNit, nombre, Municipio, Direccion, Email, Celular, TelFijo,Ext,Barrio, MedioConocio, MesCumpleaños, DiaCumpleaños)
    db.session.add(new_cli)
    db.session.commit()
  else:
    Cliente.query.filter(Cliente.cli_identificacion == CcNit).update({Cliente.cli_nombre: nombre, Cliente.cli_ciudad: Municipio , Cliente.cli_direccion: Direccion, Cliente.cli_email : Email, Cliente.cli_celular:  Celular, Cliente.cli_telefono: TelFijo, Cliente.cli_extension: Ext, Cliente.cli_barrio: Barrio, Cliente.cli_medioConocio: MedioConocio, Cliente.cli_modifica: 'current_user.usu_login', Cliente.cli_nacido_mes: MesCumpleaños, Cliente.cli_nacido_dia: DiaCumpleaños, Cliente.cli_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
    db.session.commit()
  if Factura.query.get(Consecutivo) is None:
    new_factu = Factura(nombre, TipoPedido, ReferenciaNombre, ReferenciaCelular, ReferenciaTelefono, Poblacion, TipoEvento, DiaEvento, MesEvento, AñoEvento, Referencia1, Descripcion1, Accesorios1, MedidasArreglos1, ValorReferencia1, Referencia2, Descripcion2, Accesorios2, MedidasArreglos2, ValorReferencia2, Referencia3, Descripcion3, Accesorios3, MedidasArreglos3, ValorReferencia3, Referencia4, Descripcion4, Accesorios4, MedidasArreglos4, ValorReferencia4, Total, Abono, Saldo, DiaRecoger, MesRecoger ,AñoRecoger, DiaEntregar, MesEntregar, AñoEntregar, 'current_user.usu_login', ConsecutivoManual, Nota)
    db.session.add(new_factu)
    db.session.commit()
  else:
      Factura.query.filter(Factura.fac_numero == Consecutivo).update({Factura.fac_cliente : nombre , Factura.fac_tipoPedido : TipoPedido, Factura.fac_poblacion : Poblacion , Factura.fac_evento : TipoEvento , Factura.fac_eventoDia: DiaEvento , Factura.fac_eventoMes : MesEvento , Factura.fac_eventoAño : AñoEvento, Factura.fac_ReferenciaProducto1 : Referencia1 , Factura.fac_ReferenciaProducto2 : Referencia2 , Factura.fac_ReferenciaProducto3: Referencia3, Factura.fac_ReferenciaProducto4: Referencia4, Factura.fac_descripcion1: Descripcion1, Factura.fac_descripcion2: Descripcion2, Factura.fac_descripcion3: Descripcion3, Factura.fac_descripcion4: Descripcion4, Factura.fac_accesorios1: Accesorios1, Factura.fac_accesorios2: Accesorios2, Factura.fac_accesorios3: Accesorios3, Factura.fac_accesorios4: Accesorios4, Factura.fac_MedidasArreglos1: MedidasArreglos1, Factura.fac_MedidasArreglos2: MedidasArreglos2, Factura.fac_MedidasArreglos3: MedidasArreglos3, Factura.fac_MedidasArreglos4: MedidasArreglos4, Factura.fac_ValorReferencia1: ValorReferencia1, Factura.fac_ValorReferencia2: ValorReferencia2, Factura.fac_ValorReferencia3: ValorReferencia3, Factura.fac_ValorReferencia4: ValorReferencia4, Factura.fac_ReclamarMercanciaDia : DiaRecoger, Factura.fac_ReclamarMercanciaMes : MesRecoger, Factura.fac_ReclamarMercanciaAño : AñoRecoger,Factura.fac_DevolverMercanciaDia : DiaEntregar,Factura.fac_DevolverMercanciaMes : MesEntregar, Factura.fac_DevolverMercanciaAño: AñoEntregar, Factura.fac_AtendidoPor: 'current_user.usu_login', Factura.fac_consecutivoManual: ConsecutivoManual, Factura.fac_nota : Nota},synchronize_session=False)
      db.session.commit()



  return jsonify({'nombre': Nota})
  return jsonify({'error': 'Missing data'})

@app.route('/_descargar_pdf', methods=['GET','POST'])
def descargar_pdf():

  file = 'factura.pdf'
  #return jsonify(result = True)
  nombre = request.form.get('txtNonmbreCliente')
  
  CcNit = request.form.get("txtCC_Nit")
  DiaCumpleaños = request.form.get("txtDiaCumpleaños")
  MesCumpleaños = request.form.get('txtMesCumpleaños')#[]
  TelFijo = request.form.get("txtTelefonoFijo")
  Ext = request.form.get("Ext")
  Celular = request.form.get("txtCelular")
  Email = request.form.get('txtEmail')#[]
  Direccion = request.form.get('txtDireccion')#[]
  Municipio = request.form.get('txtMunicipio')#[]
  Barrio = request.form.get('txtBarrio')#[]
  MedioConocio = request.form.get('txtMedioConocio')#[]
  #
  #
  #
  TipoPedido = request.form.get('txtTipoPedido')
  Poblacion = request.form.get('txtPedPoblacion')
  TipoEvento = request.form.get('txtTipoEvento')
  DiaEvento = request.form.get('txtDiaEvento')
  MesEvento = request.form.get('txtMesEvento')
  AñoEvento = request.form.get('txtAñoEvento')
  Referencia1 = request.form.get('txtReferencia1')
  Descripcion1 = request.form.get('txtDescripcion1')
  Accesorios1 = request.form.get('txtAccesorios1')
  MedidasArreglos1 = request.form.get('txtMedidasArreglos1')
  ValorReferencia1 = request.form.get('txtValorReferencia1')
  Referencia2 = request.form.get('txtReferencia2')
  Descripcion2 = request.form.get('txtDescripcion2')
  Accesorios2 = request.form.get('txtAccesorios2')
  MedidasArreglos2 = request.form.get('txtMedidasArreglos2')
  ValorReferencia2 = request.form.get('txtValorReferencia2')
  Referencia3 = request.form.get('txtReferencia3')
  Descripcion3 = request.form.get('txtDescripcion3')
  Accesorios3 = request.form.get('txtAccesorios3')
  MedidasArreglos3 = request.form.get('txtMedidasArreglos3')
  ValorReferencia3 = request.form.get('txtValorReferencia3')
  Referencia4 = request.form.get('txtReferencia4')
  Descripcion4 = request.form.get('txtDescripcion4')
  Accesorios4 = request.form.get('txtAccesorios4')
  MedidasArreglos4 = request.form.get('txtMedidasArreglos4')
  ValorReferencia4 = request.form.get('txtValorReferencia4')
  #
  DiaRecoger = request.form.get('txtDiaRecoger')
  MesRecoger = request.form.get('txtMesRecoger')
  AñoRecoger = request.form.get('txtAñoRecoger')
  DiaEntregar = request.form.get('txtDiaEntregar')
  MesEntregar = request.form.get('txtMesEntregar')
  AñoEntregar =  request.form.get('txtAñoEntregar')
  Saldo = request.form.get('txtSaldo')
  Total = request.form.get('txtTotal')
  Abono =  request.form.get('txtAbono')
  Retefuente = request.form.get('txtRetefuente')
  ReferenciaNombre = request.form.get('txtReferenciaNombre')#[]
  ReferenciaCelular = request.form.get('txtReferenciaCelular')#[]
  ReferenciaTelefono = request.form.get('txtReferenciaTelefono')#[]
  Nota = request.form.get('txtNota')#[]
  #
  ConsecutivoManual = request.form.get('txtConsecutivoManual')#[]z
  Consecutivo = request.form.get('txtConsecutivo')#[]z
  AtendidoPor = request.form.get('txtAtendidoPor')#[]z


  if Cliente.query.get(CcNit) is None:
    new_cli = Cliente(CcNit, nombre, Municipio, Direccion, Email, Celular, TelFijo,Ext,Barrio, MedioConocio, MesCumpleaños, DiaCumpleaños)
    db.session.add(new_cli)
    db.session.commit()
  else:
    Cliente.query.filter(Cliente.cli_identificacion == CcNit).update({Cliente.cli_nombre: nombre, Cliente.cli_ciudad: Municipio , Cliente.cli_direccion: Direccion, Cliente.cli_email : Email, Cliente.cli_celular:  Celular, Cliente.cli_telefono: TelFijo, Cliente.cli_extension: Ext, Cliente.cli_barrio: Barrio, Cliente.cli_medioConocio: MedioConocio, Cliente.cli_modifica: 'current_user.usu_login', Cliente.cli_nacido_mes: MesCumpleaños, Cliente.cli_nacido_dia: DiaCumpleaños, Cliente.cli_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
    db.session.commit()
  #if Factura.query.get(Consecutivo) is None:
  new_factu = Factura(nombre, TipoPedido, ReferenciaNombre, ReferenciaCelular, ReferenciaTelefono, Poblacion, TipoEvento, DiaEvento, MesEvento, AñoEvento, Referencia1, Descripcion1, Accesorios1, MedidasArreglos1, ValorReferencia1, Referencia2, Descripcion2, Accesorios2, MedidasArreglos2, ValorReferencia2, Referencia3, Descripcion3, Accesorios3, MedidasArreglos3, ValorReferencia3, Referencia4, Descripcion4, Accesorios4, MedidasArreglos4, ValorReferencia4, Total, Abono, Saldo, DiaRecoger, MesRecoger ,AñoRecoger, DiaEntregar, MesEntregar, AñoEntregar, 'wacor', ConsecutivoManual,Nota)
  db.session.add(new_factu)
  db.session.commit()
  #else:
   #   Factura.query.filter(Factura.fac_numero == Consecutivo).update({Factura.fac_cliente : nombre , Factura.fac__tipoPedido : TipoPedido, Factura.fac_poblacion : Poblacion , Factura.fac_evento : TipoEvento , Factura.fac_eventoDia: DiaEvento , Factura.fac_eventoMes : MesEvento , Factura.fac_eventoAño : AñoEvento, Factura.fac_ReferenciaProducto1 : Referencia1 , Factura.fac_ReferenciaProducto2 : Referencia2 , Factura.fac_ReferenciaProducto3: Referencia3, Factura.fac_ReferenciaProducto4: Referencia4, Factura.fac_descripcion1: Descripcion1, Factura.fac_descripcion2: Descripcion2, Factura.fac_descripcion3: Descripcion3, Factura.fac_descripcion4: Descripcion4, Factura.fac_accesorios1: Accesorios1, Factura.fac_accesorios2: Accesorios2, Factura.fac_accesorios3: Accesorios3, Factura.fac_accesorios4: Accesorios4, Factura.fac_MedidasArreglos1: MedidasArreglos1, Factura.fac_MedidasArreglos2: MedidasArreglos2, Factura.fac_MedidasArreglos3: MedidasArreglos3, Factura.fac_MedidasArreglos4: MedidasArreglos4, Factura.fac_ValorReferencia1: ValorReferencia1, Factura.fac_ValorReferencia2: ValorReferencia2, Factura.fac_ValorReferencia3: ValorReferencia3, Factura.fac_ValorReferencia4: ValorReferencia4, Factura.fac_ReclamarMercanciaDia : DiaRecoger, Factura.fac_ReclamarMercanciaMes : MesRecoger, Factura.fac_ReclamarMercanciaAño : AñoRecoger,Factura.fac_DevolverMercanciaDia : DiaEntregar,Factura.fac_DevolverMercanciaMes : MesEntregar, Factura.fac_DevolverMercanciaAño: AñosEntregar, Factura.fac_AtendioPor:' current_user.usu_login', Factura.fac_consecutivoManual: ConsecutivoManual, Factura.fac_nota : Nota},synchronize_session=False)
    #  db.session.commit()
  factura = Factura.query.get(5)
  #cliente = Cliente.query.get(CcNit)
  


  
  #pdf = create_pdf(render_template("factura.html", factura = factura, cliente = cliente, path = os.path.abspath(os.path.dirname(__file__))), file)
  path = 'C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/Ffactura.pdf'
  pagina = render_template("factura.html", factura = factura)
  config = api.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

  pdf = api.from_string(pagina,False,configuration=config)
  
  download('Ffactura.pdf')
  """return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-disposition:":
                 "attachment; filename=factura.html"})"""
  #response = make_response(pdf)


  #response.headers["Content-Disposition"] = "attachment; filename=Ffactura.pdf"
  #response.mimetype='application/pdf'
  #return send_from_directory('C:\\Users\\Cidenet\\Documents\\VirutalEnvs\\ikotia\\ikotia\\uploads\\pdf\\','Ffactura.pdf', as_attachment=True)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

@app.route('/retornar')
def retornar():
  return send_file('C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/Ffactura.pdf')

@app.route('/siguienteFactura', methods=['GET','POST'])
def siguienteFactura():
  
  Factura_actual = int(request.form.get('txtConsecutivo'))
  Factura_actual+1   
  factura = Factura.query.get(str(Factura_actual))
  cliente = Cliente.query.get(str(factura.fac_cliente))
  return jsonify(str(cliente.cli_nombre))
  #cliente = Cliente.query.get(str(factura.fac_cliente))   
  #return jsonify(cliente.cli_identificacion)
  """
  if factura is None:
    while (factura==None):
      str(IntentoDeEncontrarFactura)
      factura = Factura.query.get(IntentoDeEncontrarFactura)
      int(IntentoDeEncontrarFactura)
      IntentoDeEncontrarFactura+1
      cliente = Cliente.query.get(str(factura.fac_cliente))   
    return jsonify({'fac_numero':factura.fac_numero,'fac_cliente':factura.fac_cliente,'fac_tipoPedido':factura.fac_tipoPedido,'fac_ReferenciaNombre':factura.fac_ReferenciaNombre,'fac_ReferenciaCelular':factura.fac_ReferenciaCelular,'fac_ReferenciaMedio': factura.fac_ReferenciaMedio, 'fac_poblacion':factura.fac_poblacion, 'fac_evento':factura.fac_evento,'fac_eventoDia':factura.fac_eventoDia, 'fac_eventoMes':factura.fac_eventoMes, 'fac_eventoAño': factura.fac_eventoAño,'fac_ReferenciaProducto1': factura.fac_ReferenciaProducto1,'fac_ReferenciaProducto2': factura.fac_ReferenciaProducto2,'fac_ReferenciaProducto3':factura.fac_ReferenciaProducto3,'fac_ReferenciaProducto4': factura.fac_ReferenciaProducto4,'fac_descripcion1':factura.fac_descripcion1, 'fac_descripcion2':factura.fac_descripcion2,'fac_descripcion3':factura.fac_descripcion3,'fac_descripcion4':factura.fac_descripcion4, 'fac_MedidasArreglos1': factura.fac_MedidasArreglos1, 'fac_MedidasArreglos2':factura.fac_MedidasArreglos2,'fac_MedidasArreglos3': factura.fac_MedidasArreglos3, 'fac_MedidasArreglos4': factura.fac_MedidasArreglos4, 'fac_ValorReferencia1':factura.fac_ValorReferencia1, 'fac_ValorReferencia2':factura.fac_ValorReferencia2, 'fac_ValorReferencia3':factura.fac_ValorReferencia3, 'fac_ValorReferencia4': factura.fac_ValorReferencia4, 'fac_Total':factura.fac_Total, 'fac_Abono': factura.fac_Abono, 'fac_Saldo':factura.fac_Saldo, 'fac_Retefuente': factura.fac_Retefuente , 'fac_ReclamarMercanciaDia': factura.fac_ReclamarMercanciaDia, 'fac_ReclamarMercanciaMes': factura.fac_ReclamarMercanciaMes, 'fac_ReclamarMercanciaAño': factura.fac_ReclamarMercanciaAño, 'fac_DevolverMercanciaDia':factura.fac_DevolverMercanciaDia, 'fac_DevolverMercanciaMes':factura.fac_DevolverMercanciaMes, 'fac_DevolverMercanciaAño':factura.fac_DevolverMercanciaAño, 'fac_AtendidoPor': factura.fac_AtendidoPor,'fac_consecutivoManual':factura.fac_consecutivoManual,'cli_identificacion': cliente.cli_identificacion, 'cli_nombre': cliente.cli_nombre, 'cli_ciudad':cliente.cli_ciudad, 'cli_direccion': cliente.cli_direccion, 'cli_email':cliente.cli_email, 'cli_celular':cliente.cli_celular, 'cli_telefono':cliente.cli_telefono,'cli_extension':cliente.cli_extension, 'cli_cargo':cliente.cli_cargo, 'cli_barrio':cliente.cli_barrio, 'cli_medioConocio':cliente.cli_medioConocio})
  else:
    cliente = Cliente.query.get(str(factura.fac_cliente))
    
    return jsonify({'fac_numero':factura.fac_numero,'fac_cliente':factura.fac_cliente,'fac_tipoPedido':factura.fac_tipoPedido,'fac_ReferenciaNombre':factura.fac_ReferenciaNombre,'fac_ReferenciaCelular':factura.fac_ReferenciaCelular,'fac_ReferenciaMedio': factura.fac_ReferenciaMedio, 'fac_poblacion':factura.fac_poblacion, 'fac_evento':factura.fac_evento,'fac_eventoDia':factura.fac_eventoDia, 'fac_eventoMes':factura.fac_eventoMes, 'fac_eventoAño': factura.fac_eventoAño,'fac_ReferenciaProducto1': factura.fac_ReferenciaProducto1,'fac_ReferenciaProducto2': factura.fac_ReferenciaProducto2,'fac_ReferenciaProducto3':factura.fac_ReferenciaProducto3,'fac_ReferenciaProducto4': factura.fac_ReferenciaProducto4,'fac_descripcion1':factura.fac_descripcion1, 'fac_descripcion2':factura.fac_descripcion2,'fac_descripcion3':factura.fac_descripcion3,'fac_descripcion4':factura.fac_descripcion4, 'fac_MedidasArreglos1': factura.fac_MedidasArreglos1, 'fac_MedidasArreglos2':factura.fac_MedidasArreglos2,'fac_MedidasArreglos3': factura.fac_MedidasArreglos3, 'fac_MedidasArreglos4': factura.fac_MedidasArreglos4, 'fac_ValorReferencia1':factura.fac_ValorReferencia1, 'fac_ValorReferencia2':factura.fac_ValorReferencia2, 'fac_ValorReferencia3':factura.fac_ValorReferencia3, 'fac_ValorReferencia4': factura.fac_ValorReferencia4, 'fac_Total':factura.fac_Total, 'fac_Abono': factura.fac_Abono, 'fac_Saldo':factura.fac_Saldo, 'fac_Retefuente': factura.fac_Retefuente , 'fac_ReclamarMercanciaDia': factura.fac_ReclamarMercanciaDia, 'fac_ReclamarMercanciaMes': factura.fac_ReclamarMercanciaMes, 'fac_ReclamarMercanciaAño': factura.fac_ReclamarMercanciaAño, 'fac_DevolverMercanciaDia':factura.fac_DevolverMercanciaDia, 'fac_DevolverMercanciaMes':factura.fac_DevolverMercanciaMes, 'fac_DevolverMercanciaAño':factura.fac_DevolverMercanciaAño, 'fac_AtendidoPor': factura.fac_AtendidoPor,'fac_consecutivoManual':factura.fac_consecutivoManual,'cli_identificacion': cliente.cli_identificacion, 'cli_nombre': cliente.cli_nombre, 'cli_ciudad':cliente.cli_ciudad, 'cli_direccion': cliente.cli_direccion, 'cli_email':cliente.cli_email, 'cli_celular':cliente.cli_celular, 'cli_telefono':cliente.cli_telefono,'cli_extension':cliente.cli_extension, 'cli_cargo':cliente.cli_cargo, 'cli_barrio':cliente.cli_barrio, 'cli_medioConocio':cliente.cli_medioConocio})
  
  """
   #return jsonify(fac_numero = factura.fac_numero, fac_tipoPedido =Factura.fac_tipoPedido,fac_ReferenciaNombre = Factura.fac_ReferenciaNombre, fac_ReferenciaCelular =Factura.fac_ReferenciaCelular, fac_ReferenciaMedio =Factura.fac_ReferenciaMedio,  fac_poblacion =Factura.fac_poblacion)


  """
  IntentoDeEncontrarFactura = 0
  if Factura_actual is None:
    while (Factura_actual==None):

      Factura_actual = Factura.query.get(IntentoDeEncontrarFactura)
      IntentoDeEncontrarFactura+1
    Factura.query.get(Factura_actual)
    return jsonify(fac_numero = Factura.fac_numero, fac_tipoPedido =Factura.fac_tipoPedido,fac_ReferenciaNombre = Factura.fac_ReferenciaNombre, fac_ReferenciaCelular =Factura.fac_ReferenciaCelular, fac_ReferenciaMedio =Factura.fac_ReferenciaMedio,  fac_poblacion =Factura.fac_poblacion)

  else: 
    Factura_actual+1 
    Factura.query.get(Factura_actual)
    return jsonify(fac_numero = Factura.fac_numero, fac_tipoPedido =Factura.fac_tipoPedido,fac_ReferenciaNombre = Factura.fac_ReferenciaNombre, fac_ReferenciaCelular =Factura.fac_ReferenciaCelular, fac_ReferenciaMedio =Factura.fac_ReferenciaMedio,  fac_poblacion =Factura.fac_poblacion)
  
    return jsonify(fac_numero = Factura.fac_numero, fac_tipoPedido =Factura.fac_tipoPedido,fac_ReferenciaNombre = Factura.fac_ReferenciaNombre, fac_ReferenciaCelular =Factura.fac_ReferenciaCelular, fac_ReferenciaMedio =Factura.fac_ReferenciaMedio,  fac_poblacion =Factura.fac_poblacion)
  
"""


















