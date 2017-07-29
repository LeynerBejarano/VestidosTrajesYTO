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
from sqlalchemy.sql.expression import func
from flask.ext.login import login_required, current_user
from flask_wtf.file import FileField
from flask import render_template, redirect, request, jsonify, url_for, flash,send_from_directory, Flask
from flask.ext.mail import Mail, Message
from flask.ext.principal import Identity
from .form_pedido import Form_Pedido
from app.model.factura_borrador import Factura_Borrador
from datetime import datetime
from datetime import datetime, date
from num2words import num2words
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
from app.model.facturaDetalle import FacturaDetalle
from app.model.personalizada import Personalizada
from app.model.transportadora import Transportadora
from app.model.tipo_orden import Tipo_orden
from app.model.medioConocio import MedioConocio
from app.model.tipoPedido import TipoPedido
from app.model.factura import Factura
from app.model.cantidadPrenda import CantidadPrenda
from app.model.reservasPrenda import ReservasPrenda
from app.model.recibo import Recibo
from app.model.horaRecogidaReserva import HoraRecogidaReserva
from app.model.passSkill import PassSkill
from app.utils import numero_a_letras, timeRange, get_temporada, text_to_time
from pdfkit import api
from flask import make_response
from flask import send_file,Response
import locale


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
    cantidadPrenda = CantidadPrenda.query.filter(CantidadPrenda.cantidadPrenda_nombre_talla_color.like('%_%')).order_by(CantidadPrenda.cantidadPrenda_id)



    #### Creacion de arreglos usados en el auto-completar de jquery
    cedulas = []
    for cli in Cliente.query:
      cedulas.append(int(cli.cli_identificacion))

    form = Form_Pedido()

    #### Agregar entradas a los FieldList solo cuando se carga la pagina, para evitar datos duplicados en la validacion

    
        

    ### Volcado de datos en el fieldlist Detalles

    

      

      ###Estilos

    ##fecha actual
    hoy = "{:%d.%m.%Y}".format(datetime.now())

      




    choices = [(v.usu_login, v.usu_nombre + ' ' + v.usu_apellido if v.usu_estado == 1 else 'Inactivo - ' + v.usu_nombre + ' ' + v.usu_apellido) for v in vendedores]
    form.vendedor.choices = choices
    choices = [(ti.pedi_id, ti.pedi_nombre) for ti in tipoPedido or []] + [(-1, 'Otro')]
    form.fac_tipoPedido.choices = choices
    form.fac_tipoPedido.default = 8
    form.process()
    choices = [(m.medio_id, m.medio_nombre) for m in medioConocio or []] + [(-1, 'Otro')]
    form.cli_medioConocio.choices = choices
    choices = [(c.ciu_id, c.ciu_nombre) for c in ciudades or []] + [(-1, 'Otro')]
    form.ciudad.choices = choices
    form.ciudad.default = 16
    form.process()
    form.ins_ciudad.choices = choices
    choices = [(e.eve_id, e.eve_nombre) for e in eventos or []] + [(-1, 'Otro')]
    form.ped_evento.choices = choices
    choices = [(t.tip_id, t.tip_nombre) for t in tipos_orden or []]
    form.ent_tipo_orden.choices = choices
    form.rec_tipo_orden.choices = choices
    form.tipo_entrega_ord.choices = choices
    form.tipo_recogida_ord.choices = choices
    choices = [(c.cantidadPrenda_id, c.cantidadPrenda_nombre_talla_color) for c in cantidadPrenda or []]
    form.fac_prenda.choices = choices
    choices = [(c.cla_id - 1, c.cla_id - 1) for c in clases or []]
    form.principal.choices = choices
    form.dia_enc.choices = [(i, str(i)) for i in range(1,32) or []]
    form.dia_Entregar.choices = [(i, str(i)) for i in range(1,32) or []]
    form.dia_Devolver.choices = [(i, str(i)) for i in range(1,32) or []]
    form.año_Entregar.choices = [(i, str(i)) for i in range(2014,2023) or []]
    form.año_Devolver.choices = [(i, str(i)) for i in range(2014,2023) or []]
    
      

    ####### SUBMIT ######
    
    
    usuario = current_user.usu_login 
    if usuario:
      return render_template('pedido.html',datos = datos,hoy = hoy, form = form ,clases = clases,tallas = tallas, cedulas = cedulas,cliente = request.args.get('cliente'),pedido = request.args.get('pedido'))

@app.route('/insertarCliente', methods=['GET','POST'])
def insertarCliente():

  
  nombre = request.form.get('txtNonmbreCliente')
  
  CcNit = request.form.get("txtCC_Nit")
  DiaCumpleaños = request.form.get("txtDiaCumpleaños")
  MesCumpleaños = request.form.get('txtMesCumpleaños')#[]
  TelFijo = request.form.get("txtTelefonoFijo")
  Ext = request.form.get("Ext")
  TelFijoOficina = request.form.get("txtTelefonoFijoOficina")
  ExtOficina = request.form.get("ExtOficina")
  Celular = request.form.get("txtCelular")
  Email = request.form.get('txtEmail')#[]
  Direccion = request.form.get('txtDireccion')#[]
  if(str(request.form.get('txtMunicipio')).isdigit()):
    Municipio = request.form.get('txtMunicipio')
  else:
    Municipio = Ciudad.query.filter(Ciudad.ciu_nombre == str(request.form.get('txtMunicipio'))).all()[0].ciu_id
  Barrio = request.form.get('txtBarrio')#[]
  if(str(request.form.get('txtMedioConocio')).isdigit()):
    MedioConocio = request.form.get('txtMedioConocio')
  else:
    MedioConocio = MedioConocio.query.filter(MedioConocio.medio_nombre == str(request.form.get('txtMedioConocio'))).all()[0].medio_id
  Poblacion = request.form.get('txtPedPoblacion')
  #
  #
  #
  TipoPedido = request.form.get('txtTipoPedido')
  if(str(request.form.get('txtTipoEvento')).isdigit()):
    TipoEvento = request.form.get('txtTipoEvento')
  else:
    TipoEvento = Evento.query.filter(Evento.eve_nombre == str(request.form.get('txtTipoEvento'))).all()[0].eve_id
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
  Abono =  request.form.get('txtAbono')
  Retefuente = request.form.get('txtRetefuente')
  ReferenciaNombre = request.form.get('txtReferenciaNombre')#[]
  ReferenciaCelular = request.form.get('txtReferenciaCelular')#[]
  ReferenciaTelefono = request.form.get('txtReferenciaTelefono')#[]
  Nota = request.form.get('txtNota')#[]
  #
  ConsecutivoManual = request.form.get('txtConsecutivoManual')#[]z
  Consecutivo = request.form.get('txtConsecutivo')#[]z
  ConsecutivoActual = request.form.get('txtConsecutivoActual')
  hoy = "{:%d.%m.%Y}".format(datetime.now())
  fac_fechaFactura = hoy
  fac_horasCadaReclamarMH = request.form.get('txtHoraReclamarA')
  fac_horasReclamarCadaH = request.form.get('txtHoraReclamarB')
  fac_horasDevolverCadaH  = request.form.get('txtHoraDevolverB')
  fac_horasCadaDevolverMH = request.form.get('txtHoraDevolverA')
  eventoFecha = str(request.form.get('txtfechaEvento'))
  Retefuente = request.form.get('txtRetefuente')
  fac_eventoFecha = str(request.form.get('txtfechaEvento'))
  fac_ReclamarMercanciaFecha = str(request.form.get('txtfechaRecoger'))
  fac_DevolverMercanciaFecha  = str(request.form.get('txtfechaDevolver'))
  fac_horasDevolverCadaH = request.form.get('txtHoraDevolverB')
  fac_horasReclamarCadaH = request.form.get('txtHoraReclamarB')
  fac_horasCadaDevolverMH   = request.form.get('txtHoraDevolverA')
  fac_horasCadaReclamarMH = request.form.get('txtHoraReclamarA')
  fac_CantidadLLeva1 = request.form.get('cantidadRealPrenda1')
  fac_CantidadLLeva2 = request.form.get('cantidadRealPrenda2')
  fac_CantidadLLeva3 = request.form.get('cantidadRealPrenda3')
  fac_CantidadLLeva4 = request.form.get('cantidadRealPrenda4')
  Total = 0
  
  for a in request.form.getlist('txtValorReferenciaArray[]',type= str):
    if a:
      Total = Total + int(a)
  #######
  ######
  #######
  ######
  if(fac_eventoFecha[0:3] == "201" ):
    fac_eventoFecha=date(int(fac_eventoFecha[0:4]),int(fac_eventoFecha[5:7]),int(fac_eventoFecha[8:10]))
  else:
    fac_eventoFecha= date(int(fac_eventoFecha[6:10]), int(fac_eventoFecha[3:5]), int(fac_eventoFecha[0:2]))
  if(fac_ReclamarMercanciaFecha[0:3] == "201" ):
    fac_ReclamarMercanciaFecha=date(int(fac_ReclamarMercanciaFecha[0:4]),int(fac_ReclamarMercanciaFecha[5:7]),int(fac_ReclamarMercanciaFecha[8:10]))
  else:
    fac_ReclamarMercanciaFecha= date(int(fac_ReclamarMercanciaFecha[6:10]),int(fac_ReclamarMercanciaFecha[3:5]), int(fac_ReclamarMercanciaFecha[0:2]))
  if(fac_DevolverMercanciaFecha[0:3] == "201" ):
    fac_DevolverMercanciaFecha=date(int(fac_DevolverMercanciaFecha[0:4]),int(fac_DevolverMercanciaFecha[5:7]),int(fac_DevolverMercanciaFecha[8:10]))
  else:
    fac_DevolverMercanciaFecha= date(int(fac_DevolverMercanciaFecha[6:10]), int(fac_DevolverMercanciaFecha[3:5]), int(fac_DevolverMercanciaFecha[0:2]))


  if Cliente.query.get(CcNit) is None:
    new_cli = Cliente(CcNit, nombre, Municipio, Direccion, Email, Celular, TelFijo, Ext, TelFijoOficina , ExtOficina, Barrio, MedioConocio, MesCumpleaños, DiaCumpleaños)
    db.session.add(new_cli)
    db.session.commit() 
  else:
    Cliente.query.filter(Cliente.cli_identificacion == CcNit).update({Cliente.cli_nombre: nombre, Cliente.cli_ciudad: Municipio , Cliente.cli_direccion: Direccion, Cliente.cli_email : Email, Cliente.cli_celular:  Celular, Cliente.cli_telefono: TelFijo, Cliente.cli_extension: Ext, Cliente.cli_telefonoFijo: TelFijoOficina, Cliente.cli_telefonoFijo_ext: ExtOficina,Cliente.cli_barrio: Barrio, Cliente.cli_medioConocio: MedioConocio, Cliente.cli_modifica: current_user.usu_login , Cliente.cli_nacido_mes: MesCumpleaños, Cliente.cli_nacido_dia: DiaCumpleaños, Cliente.cli_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
    db.session.commit()
  if Factura.query.get(Consecutivo) is None:
    new_factu = Factura(CcNit, TipoPedido, ReferenciaNombre, ReferenciaCelular, ReferenciaTelefono, Poblacion, TipoEvento, fac_eventoFecha, DiaEvento, MesEvento, AñoEvento,  Total, Total, Retefuente, fac_ReclamarMercanciaFecha,fac_horasReclamarCadaH, fac_horasCadaReclamarMH, DiaRecoger, MesRecoger ,AñoRecoger, fac_horasDevolverCadaH, fac_DevolverMercanciaFecha,fac_horasCadaDevolverMH, DiaEntregar, MesEntregar, AñoEntregar, current_user.usu_nombre ,ConsecutivoManual,Nota)
    db.session.add(new_factu)
    db.session.commit()
    if request.form.get('txtHoraReclamarB') is None:
      request.form.get('txtHoraReclamarA')
      new_hora = HoraRecogidaReserva(fac_ReclamarMercanciaFecha,None,int(request.form.get('txtHoraReclamarA')))
      db.session.add(new_hora)
      db.session.commit()
    else:
      new_hora = HoraRecogidaReserva(fac_ReclamarMercanciaFecha,None,int(request.form.get('txtHoraReclamarB')))
      db.session.add(new_hora)
      db.session.commit()
      for a in range(len(request.form.getlist('ReferenciaPrendaArray[]',type= str))):
        factuDetalle = FacturaDetalle(int(request.form.get('txtConsecutivoActual')),int(request.form.getlist('ReferenciaPrendaArray[]',type= str)[a-1]),request.form.getlist('txtDescripcionArray[]',type= str )[a],request.form.getlist('txtAccesoriosArray[]', type = str)[a],str(request.form.getlist('txtMedidasArreglosArray[]', type = str)[a]),request.form.getlist('EstiloArray[]', type = str)[a],int(request.form.getlist('txtValorReferenciaArray[]', type = str)[a]),request.form.getlist('LineaSexoArray[]', type = str)[a])
        db.session.add(factuDetalle)
        db.session.commit()
        if(int(TipoPedido) % 2 == 0):
          if(int(request.form.getlist('ReferenciaPrendaArray[]',type= str)[a]) is not None and fac_ReclamarMercanciaFecha is not None and fac_DevolverMercanciaFecha is not None and  ConsecutivoActual is not None):
            reserva = ReservasPrenda(int(request.form.getlist('ReferenciaPrendaArray[]',type= str)[a]), fac_ReclamarMercanciaFecha,  fac_DevolverMercanciaFecha, ConsecutivoActual)
            db.session.add(reserva)
            db.session.commit()
  else:
    if(str(current_user.usu_login) != "john"):
      Factura.query.filter(Factura.fac_numero == Consecutivo).update({Factura.fac_cliente : CcNit , Factura.fac_tipoPedido : TipoPedido, Factura.fac_poblacion : Poblacion , Factura.fac_evento : TipoEvento , Factura.fac_eventoDia: DiaEvento , Factura.fac_eventoMes : MesEvento , Factura.fac_eventoAño : AñoEvento,Factura.fac_horasReclamarCadaH: fac_horasReclamarCadaH, Factura.fac_horasCadaReclamarMH: fac_horasCadaReclamarMH,  Factura.fac_horasDevolverCadaH: fac_horasDevolverCadaH,Factura.fac_horasCadaDevolverMH: fac_horasCadaDevolverMH, Factura.fac_DevolverMercanciaDia : DiaEntregar,Factura.fac_DevolverMercanciaMes : MesEntregar, Factura.fac_DevolverMercanciaAño: AñoEntregar, Factura.fac_AtendidoPor: current_user.usu_login, Factura.fac_consecutivoManual: ConsecutivoManual, Factura.fac_nota : Nota, Factura.fac_Total:Total, },synchronize_session=False)
      db.session.commit()
    else:
      if (Recibo.query.filter(Recibo.reci_Factura == int(request.form.get('txtConsecutivoActual'))).all() is None):
        Factura.query.filter(Factura.fac_numero == Consecutivo).update({Factura.fac_Saldo : Total},synchronize_session=False)
        db.session.commit()
  


  """
  entonces necesito Cambiar

      
  """


  return jsonify(request.form.getlist('LineaSexoArray[]', type = str))
  
 

@app.route('/descargar_recibo', methods=['GET','POST'])
def descargar_recibo():

  file = 'factura.pdf'
  #return jsonify(result = True)
  Consecutivo = request.form.get('ConsecutivoN')
  
  recibo = Recibo.query.get(int(request.form.get('reciboNumero')))  
  cliente = Cliente.query.get(request.form.get('txtCC_Nit'))
  hoy = "{:%d.%m.%Y}".format(datetime.now())
  reciTipoPedido = TipoPedido.query.get(recibo.reci_FacturaTipo)
  reciTipoPedido = reciTipoPedido.pedi_nombre
  ciudad = Ciudad.query.get(cliente.cli_ciudad)




  
  #pdf = create_pdf(render_template("factura.html", factura = factura, cliente = cliente, path = os.path.abspath(os.path.dirname(__file__))), file)

  path = 'C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/FRecibofactura.pdf'
  pagina = render_template("recibo.html", recibo = recibo, cliente= cliente,hoy = hoy, reciTipoPedido = reciTipoPedido,ciudad = ciudad.ciu_nombre)
  config = api.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

  pdf = api.from_string(pagina,False,configuration=config)
  
 
  return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-disposition:":
                 "attachment; filename=factura.html"})

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
  TelFijoOficina = request.form.get("txtTelefonoFijoOficina")
  ExtOficina = request.form.get("ExtOficina")
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

  factura = Factura.query.get(111)
  cliente = Cliente.query.get(CcNit)
  hoy = "{:%d.%m.%Y}".format(datetime.now())


  
  #pdf = create_pdf(render_template("factura.html", factura = factura, cliente = cliente, path = os.path.abspath(os.path.dirname(__file__))), file)
  path = 'C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/Ffactura.pdf'
  pagina = render_template("factura.html", factura = factura, cliente= cliente,hoy = hoy)
  config = api.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

  pdf = api.from_string(pagina,False,configuration=config)
  
 
  return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-disposition:":
                 "attachment; filename=factura.html"})
  """"""
  #response = make_response(pdf)


  #response.headers["Content-Disposition"] = "attachment; filename=Ffactura.pdf"
  #response.mimetype='application/pdf'
  #return send_from_directory('C:\\Users\\Cidenet\\Documents\\VirutalEnvs\\ikotia\\ikotia\\uploads\\pdf\\','Ffactura.pdf', as_attachment=True)

#@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
#def download(filename):
#    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
 #   return send_from_directory(directory=uploads, filename=filename)

@app.route('/retornar')
def retornar():
  return send_file('C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/Ffactura.pdf')

@app.route('/siguienteFactura', methods=['GET','POST'])
def siguienteFactura():
  
  Factura_actual = int(request.form.get('txtConsecutivo'))
  Factura_actual+1   
  factura = Factura.query.get(str(Factura_actual))
  cliente = Cliente.query.get(str(factura.fac_cliente))
  recibo = Recibo.query.filter(Recibo.reci_Factura == int(Factura_actual)).all
  MesReclamar = str(factura.fac_ReclamarMercanciaFecha.month)
  DiaReclamar = str(factura.fac_ReclamarMercanciaFecha.day)
  MesDevolver = str(factura.fac_DevolverMercanciaFecha.month)
  DiaDevolver = str(factura.fac_DevolverMercanciaFecha.day)
  if(len(str(factura.fac_ReclamarMercanciaFecha.month)) < 2):
    MesReclamar = "0"+str(factura.fac_ReclamarMercanciaFecha.month)
  if(len(str(factura.fac_ReclamarMercanciaFecha.day)) < 2):
    DiaReclamar = "0"+str(factura.fac_ReclamarMercanciaFecha.day)
  if(len(str(factura.fac_DevolverMercanciaFecha.month)) < 2):
    MesDevolver = "0"+str(factura.fac_DevolverMercanciaFecha.month)
  if(len(str(factura.fac_DevolverMercanciaFecha.day)) < 2):
    DiaDevolver = "0"+str(factura.fac_DevolverMercanciaFecha.day)
  fechaInicio = str(factura.fac_ReclamarMercanciaFecha.year)+"/"+MesReclamar+"/"+DiaReclamar
  fechaFinal = str(factura.fac_DevolverMercanciaFecha.year)+"/"+MesDevolver+"/"+DiaDevolver
  ReferenciaLista = []
  DescripcionLista = []
  AccesoriosLista = []
  MedidasYarreglos = []
  EstilosLista = []
  ValorREferencia = []
  LineaSExo = []
  if(str(current_user.usu_login) != "john"):
    invalidar = "si"
  else:
    invalidar = "no"
  for lista in FacturaDetalle.query.filter(FacturaDetalle.facdet_Factura==Factura_actual).all():
    ReferenciaLista.append(lista.facdet_Referencia)
    DescripcionLista.append(lista.facdet_Descripcion)
    AccesoriosLista.append(lista.facdet_Accesorios) 
    MedidasYarreglos.append(lista.facdet_MedidasyArreglos)
    EstilosLista.append(lista.facdet_estilo) 
    ValorREferencia.append(lista.facdet_precio) 
    LineaSExo.append(lista.facdet_linea) 

  
  return jsonify({'cli_nacido_dia':cliente.cli_nacido_dia,'cli_nacido_mes':cliente.cli_nacido_mes,'fechaFinal':fechaFinal,'fechaInicio':fechaInicio,'invalidar':invalidar,'LineaSExo':LineaSExo,'ValorREferencia':ValorREferencia,'EstilosLista':EstilosLista,'MedidasYarreglos':MedidasYarreglos,'AccesoriosLista':AccesoriosLista,'DescripcionLista':DescripcionLista,'ReferenciaLista':ReferenciaLista,'fac_numero':str(factura.fac_numero),'fac_cliente':str(factura.fac_cliente),'fac_tipoPedido':str(factura.fac_tipoPedido),'fac_ReferenciaNombre':str(factura.fac_ReferenciaNombre),'fac_ReferenciaCelular':str(factura.fac_ReferenciaCelular),'fac_ReferenciaMedio': str(factura.fac_ReferenciaMedio), 'fac_poblacion':str(factura.fac_poblacion), 'fac_evento':str(factura.fac_evento),'fac_eventoFecha':str(factura.fac_eventoFecha), 'fac_eventoDia':str(factura.fac_eventoDia), 'fac_eventoMes':str(factura.fac_eventoMes), 'fac_eventoAño': str(factura.fac_eventoAño), 'fac_Total':factura.fac_Total,  'fac_Saldo':factura.fac_Saldo, 'fac_Retefuente': factura.fac_Retefuente ,'fac_ReclamarMercanciaFecha':factura.fac_ReclamarMercanciaFecha,  'fac_DevolverMercanciaDia':factura.fac_DevolverMercanciaDia, 'fac_DevolverMercanciaMes':factura.fac_DevolverMercanciaMes, 'fac_DevolverMercanciaAño':factura.fac_DevolverMercanciaAño,'fac_DevolverMercanciaFecha':factura.fac_DevolverMercanciaFecha , 'fac_AtendidoPor': factura.fac_AtendidoPor,'fac_consecutivoManual':str(factura.fac_consecutivoManual),'cli_identificacion': cliente.cli_identificacion, 'cli_nombre': cliente.cli_nombre, 'cli_ciudad':cliente.cli_ciudad, 'cli_direccion': cliente.cli_direccion, 'cli_email':cliente.cli_email, 'cli_celular':cliente.cli_celular, 'cli_telefono':cliente.cli_telefono,'cli_extension':cliente.cli_extension,'cli_telefonoOfi':cliente.cli_telefonoFijo,'cli_ExtOfi':cliente.cli_telefonoFijo_ext ,'cli_cargo':cliente.cli_cargo, 'cli_barrio':cliente.cli_barrio, 'cli_medioConocio':cliente.cli_medioConocio,'fac_fechaFactura':factura.fac_fechaFactura})

@app.route('/CuantosRecibos', methods=['GET','POST'])
def CuantosRecibos():
  Factura_actual = int(request.form.get('txtConsecutivo'))
  Factura_actual+1   
  recibo = len(Recibo.query.filter(Recibo.reci_Factura == int(Factura_actual)).all())
  return jsonify(recibo) 

@app.route('/MostrarRecibo', methods=['GET','POST'])
def MostrarRecibo():
  Factura_actual = int(request.form.get('txtConsecutivo'))  
  txtReciboActual_Relacivo = int(request.form.get('txtReciboActual_Relacivo')) - 1
  recibo = Recibo.query.filter(Recibo.reci_Factura == int(Factura_actual)).all()[txtReciboActual_Relacivo]
  ciudad = Ciudad.query.get(recibo.reci_ciudad)
  Ciudad_Fecha = str(ciudad.ciu_nombre)+' '+str(recibo.reci_fecha) 
  return jsonify({'fechaInicio':fechaInicio,'fechaFinal':fechaFinal,'reci_numero':str(recibo.reci_numero),'reci_Factura':str(recibo.reci_Factura),'reci_valor':str(recibo.reci_valor),'reci_ciudad':str(recibo.reci_ciudad),'reci_fecha':str(recibo.reci_fecha),'reci_Total': str(recibo.reci_Total), 'reci_AporteEnLetras':str(recibo.reci_AporteEnLetras), 'reci_Concepto':str(recibo.reci_Concepto),'reci_FacturaTipo':str(recibo.reci_FacturaTipo), 'reci_nuevoSaldo':str(recibo.reci_nuevoSaldo), 'reci_CCNit': str(recibo.reci_CCNit), 'Ciudad_Fecha': Ciudad_Fecha, 'RecibimosDe': str(recibo.reci_RecibimosDe)})

@app.route('/NuevoSaldo', methods=['GET','POST'])
def NuevoSaldo():

 valor_recibo = int(request.form.get('txtReciValor')) 
 Factura_actual = int(request.form.get('txtConsecutivo')) 
 factura = Factura.query.get(str(Factura_actual))
 return jsonify(int(factura.fac_Saldo)-valor_recibo)

 
@app.route('/UsuarioNuevoViejo', methods=['GET','POST'])
def UsuarioNuevoViejo():
  
  CcNit = request.form.get("txtCC_Nit")
  cliente = Cliente.query.get(CcNit)
  if Cliente.query.get(CcNit) is not None:
    return jsonify({'antiguedad':"viejo",'nombre':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_nombre,
      'ciudad':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_ciudad,
      'direccion':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_direccion,
      'email':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_email,
      'celular':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_celular,
      'telefono':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_telefono,
      'extension':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_extension,
      'telefonoFijo':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_telefonoFijo,
      'telefonoFijo_ext':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_telefonoFijo_ext,
      'barrio':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_barrio,
      'medioConocio':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_medioConocio,
      'nacido_dia':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_nacido_dia,
      'nacido_mes':Cliente.query.filter(Cliente.cli_identificacion == CcNit).all()[0].cli_nacido_mes
      })
  else:
    return jsonify({'antiguedad':"nuevo"})

@app.route('/FechaEntreFechas', methods=['GET','POST'])
def FechaEntreFechas(start, end, delta):
  curr = start
  while curr < end:
      yield curr
      curr += delta

@app.route('/GuardarRecibo', methods=['GET','POST'])
def GuardarRecibo():
  
  reci_Factura = request.form.get('txtConsecutivo')
  reci_valor = request.form.get('txtReciValor')
  hoy = datetime.now()
  reci_Total = request.form.get('txtTotal')
  reci_ciudad = request.form.get('txtMunicipio')
  reci_RecibimosDe = request.form.get('txtCC_Nit')
  reci_AporteEnLetras = request.form.get('txtReciSuSaldoEnLetras')
  reci_Concepto = request.form.get('txtReciPorconceptode')
  reci_FacturaTipo = request.form.get('txtTipoPedido')
  reci_nuevoSaldo = request.form.get('txtReciSuNuevoSaldoEs')
  reci_CCNit = request.form.get('txtReciSuNuevoSaldoEs')
  
  new_reci = Recibo(reci_Factura,reci_valor,reci_ciudad, hoy,reci_Total,reci_AporteEnLetras,reci_Concepto,reci_FacturaTipo,reci_nuevoSaldo,reci_CCNit, reci_RecibimosDe)
  db.session.add(new_reci)
  db.session.commit()
  Factura.query.filter(Factura.fac_numero == reci_Factura).update({Factura.fac_Saldo: reci_nuevoSaldo}, synchronize_session=False)
  db.session.commit()

  return jsonify(hoy)

@app.route('/ReciboPorConceptoDe', methods=['GET','POST'])
def ReciboPorConceptoDe():
  reci_Factura = int(request.form.get('txtConsecutivo'))
  valor_Recibo = int(request.form.get('txtReciValor'))
  catidadRealProductoPaVender = int(Factura.query.filter(Factura.fac_numero == int(reci_Factura)).all()[0].fac_Saldo)
  if(valor_Recibo  > catidadRealProductoPaVender):  
   return jsonify("el recibo es mayor a lo que falta en la fsctura")
  else:
    if(valor_Recibo -catidadRealProductoPaVender < 0):
      return jsonify("abono")
    else:
      return jsonify("cancelacion")

@app.route('/NumeroEnLetras', methods=['GET','POST'])
def NumeroEnLetras():
  valor_Recibo = int(request.form.get('txtReciValor')) 
  return jsonify(num2words(valor_Recibo, lang='es'))
  
@app.route('/FacturaActual', methods=['GET','POST'])
def FacturaActual():
  return jsonify({'uno':str(int(str(db.session.query(db.func.max(Factura.fac_numero)).all()[0]).replace("(", "").replace(")", "").replace(",", ""))+1)})

  

@app.route('/GenerarInformeTaller', methods=['GET','POST'])
def GenerarInformeTaller():
  FechaTallerInicio= request.form.get('txtFechaTallerInicio')
  FechaTallerInicio = date(int(FechaTallerInicio[6:10]), int(FechaTallerInicio[3:5]), int(FechaTallerInicio[0:2]))
  FechaTallerFinal= request.form.get('txtFechaTallerFinal')
  FechaTallerFinal = date(int(FechaTallerFinal[6:10]), int(FechaTallerFinal[3:5]), int(FechaTallerFinal[0:2]))
  ListaFacturas = Factura.query.filter(Factura.fac_ReclamarMercanciaFecha > FechaTallerInicio).filter(Factura.fac_ReclamarMercanciaFecha < FechaTallerFinal).all()
  ListFechaEntregar = []
  ListaHoraEntregar = []
  ListaFacturaNumero = []
  ListaDescripcion = []
  ListaAccesorios = []
  ListaMedidasArreglos = []
  ListaEstilos = []
  ListaReferencia = []

  for a in range (len(ListaFacturas)):
    for z in FacturaDetalle.query.filter(FacturaDetalle.facdet_Factura==ListaFacturas[a].fac_numero).all():
      ListaMedidasArreglos.append(z.facdet_MedidasyArreglos)
      ListaAccesorios.append(facdet_Accesorios)
      ListaDescripcion.append(z.facdet_Descripcion)
      ListaFacturaNumero.append(z.facdet_Factura)
      ListFechaEntregar.append(ListaFacturas[a].fac_ReclamarMercanciaFecha)
      ListaEstilos.append(z.facdet_estilo)
      ListaReferencia.append(z.facdet_Referencia)
      if ListaFacturas[a].fac_horasReclamarCadaH:
        if (ListaFacturas[a].fac_horasReclamarCadaH <= 11):
          ListaHoraEntregar.append(str(ListaFacturas[a].fac_horasReclamarCadaH)+"am")
        if (ListaFacturas[a].fac_horasReclamarCadaH > 11):
          ListaHoraEntregar.append(str(ListaFacturas[a].fac_horasReclamarCadaH-12)+"pm")
      else:
        if(ListaFacturas[a].fac_horasCadaReclamarMH <= 11):
          ListaHoraEntregar.append(str(ListaFacturas[a].fac_horasCadaReclamarMH)+"am")
        if(ListaFacturas[a].fac_horasReclamarCadaMH > 11):
          ListaHoraEntregar.append(str(ListaFacturas[a].fac_horasCadaReclamarMH-12)+"pm")

       

  #pdf = create_pdf(render_template("factura.html", factura = factura, cliente = cliente, path = os.path.abspath(os.path.dirname(__file__))), file)
  path = 'C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/InformeTaller.pdf'
  pagina = render_template("Informe_Taller.html", ListFechaEntregar  = ListFechaEntregar,ListaHoraEntregar = ListaHoraEntregar,ListaFacturaNumero = ListaFacturaNumero,ListaDescripcion = ListaDescripcion,ListaAccesorios  = ListaAccesorios ,ListaMedidasArreglos =ListaMedidasArreglos, ListaReferencia=ListaReferencia,ListaEstilos=ListaEstilos)
  config = api.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

  pdf = api.from_string(pagina,False,configuration=config)
  
 
  return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-disposition:":
                 "attachment; filename=InformeTaller.pdf"})


@app.route('/GenerarInformeDiarioVersionUno', methods=['GET','POST'])
def GenerarInformeDiarioVersionUno():
  rango = int(request.form.get('txtRangoInformeDiario'))
  FechaDiarioInicio = (date.today()-timedelta(days=1)).isoformat()
  FechaDiarioFinal = date.today()

  Total = 0
  TotalSemanal = 0
  TotalMensual = 0
  TotalAnual = 0
  Saldo = 0

  ListaFacturasDiarios = Factura.query.filter(Factura.fac_ReclamarMercanciaFecha > FechaTallerInicio).filter(Factura.fac_ReclamarMercanciaFecha < FechaTallerFinal).all()
  
  FechaDiarioInicio = (date.today()-timedelta(days=7)).isoformat()
  ListaFacturasSemana = Factura.query.filter(Factura.fac_ReclamarMercanciaFecha > FechaTallerInicio).filter(Factura.fac_ReclamarMercanciaFecha < FechaTallerFinal).all()
  for a in ListaFacturasSemana:
    TotalSemanal = TotalSemanal + a.fac_Total
  FechaDiarioInicio = (date.today()-timedelta(days=30)).isoformat()
  ListaFacturasMensual = Factura.query.filter(Factura.fac_ReclamarMercanciaFecha > FechaTallerInicio).filter(Factura.fac_ReclamarMercanciaFecha < FechaTallerFinal).all()
  for b in ListaFacturasMensual:
    TotalMensual = TotalMensual + b.fac_Total
  FechaDiarioInicio = (date.today()-timedelta(days=365)).isoformat()
  ListaFacturasAnual = Factura.query.filter(Factura.fac_ReclamarMercanciaFecha > FechaTallerInicio).filter(Factura.fac_ReclamarMercanciaFecha < FechaTallerFinal).all()
  for c in ListaFacturasMensual:
    TotalAnual = TotalAnual + c.fac_Total

  for a in ListaFacturasDiarios:
    Saldo = Saldo + a.fac_Saldo
    Total = Total + a.fac_Total

  path = 'C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/InformeDiario.pdf'
  pagina = render_template("InformeDiarioVersionUno.html", ListaFacturasDiarios = ListaFacturasDiarios,Total = Total, Saldo = Saldo,TotalSemanal = TotalSemanal,TotalAnual = TotalAnual,TotalMensual =TotalMensual)
  config = api.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

  pdf = api.from_string(pagina,False,configuration=config)
  
 
  return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-disposition:":
                 "attachment; filename=factura.html"})   

@app.route('/GenerarInformeDiarioVersionFoto', methods=['GET','POST'])
def GenerarInformeDiarioVersionFoto():

  now = date.today()
  FechaDiarioFinal = date(now.year,now.month,now.day)
  #"Thu, 01 Feb 2018 00:00:00 GMT"
  FechaDiarioInicio = FechaDiarioFinal-timedelta(days=1)
  ValoresFactura = []
  #"Tue, 02 Jan 2018 00:00:00 GMT"
  if(now.strftime("%A") =="Monday"):
    FechaDiarioInicioSemana = FechaDiarioFinal
  if(now.strftime("%A") =="Tuesday"):
    FechaDiarioInicioSemana = FechaDiarioFinal -timedelta(days=1)
  if(now.strftime("%A") =="Wednesday"):
    FechaDiarioInicioSemana = FechaDiarioFinal - timedelta(days=2)
  if(now.strftime("%A") =="Thursday"):
    FechaDiarioInicioSemana = FechaDiarioFinal - timedelta(days=3)
  if(now.strftime("%A") =="Friday"):
    FechaDiarioInicioSemana = FechaDiarioFinal - timedelta(days=4)
  if(now.strftime("%A") =="Saturday"):
    FechaDiarioInicioSemana = FechaDiarioFinal - timedelta(days=5)
  if(now.strftime("%A") =="Sunday"):
    FechaDiarioInicioSemana = FechaDiarioFinal - timedelta(days=6)

  if(now.day == 1):
    FechaDiarioInicioMensual = date.today()
  else:
    FechaDiarioFinalMensual  = date(now.year,now.month,(now.day-1))

  if(now.day == 1 and now.day == 1):
    FechaDiarioInicioAnual = date.today()
  else:  
    FechaDiarioInicioAnual = date(now.year,(now.month-1),(now.day-1))
  TotalFactura = 0
  TotalRecibo = 0
  SaldoFactura = 0
  TotalSemanal = 0
  TotalMensual = 0
  TotalAnual = 0




  recibo = Recibo.query.filter(Recibo.reci_fecha >= FechaDiarioInicio).filter(Recibo.reci_fecha <= FechaDiarioFinal).all()
  for a in recibo:
    TotalRecibo = TotalRecibo + a.reci_valor
  
  facturaSemanal = Factura.query.filter(Factura.fac_fechaFactura >= FechaDiarioInicioSemana).filter(Factura.fac_fechaFactura <= FechaDiarioFinal).all()
  for c in facturaSemanal:
    TotalSemanal = TotalSemanal + c.fac_Total

  FechaDiarioInicioMensual = FechaDiarioFinal-timedelta(days=30)
  facturaMensual = Factura.query.filter(Factura.fac_fechaFactura >= date(now.year,now.month,1)).filter(Factura.fac_fechaFactura <= FechaDiarioFinalMensual).all()
  for d in facturaMensual:
    TotalMensual = TotalMensual + d.fac_Total

  
  facturaAnual = Factura.query.filter(Factura.fac_fechaFactura >= FechaDiarioInicioAnual).filter(Factura.fac_fechaFactura <= FechaDiarioFinal).all()
  for e in facturaAnual:
    TotalAnual = TotalAnual + e.fac_Total

  FechaDiarioInicio = FechaDiarioFinal-timedelta(days=1)
  factura = Factura.query.filter(Factura.fac_fechaFactura >= FechaDiarioInicio).filter(Factura.fac_fechaFactura <= FechaDiarioFinal).all()
  for b in factura:
    TotalFactura = TotalFactura + b.fac_Total
    ValoresFactura.append(b.fac_Total)

  if(len(factura) > len(recibo)):
    TotalDeColumnas = len(factura)
  else:
    TotalDeColumnas = len(recibo)

     

  
  path = 'C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/InformeDiario.pdf'
  pagina = render_template("InformeDiarioVersionFoto.html",ValoresFactura= ValoresFactura, TotalDeColumnas = TotalDeColumnas,TotalAnual=TotalAnual,TotalMensual = TotalMensual,TotalSemanal =TotalSemanal, factura = factura, recibo = recibo,TotalFactura =TotalFactura,TotalRecibo = TotalRecibo,dia= now.day, mes=now.month, año= now.year )
  config = api.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

  pdf = api.from_string(pagina,False,configuration=config)
  
 
  return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-disposition:":
                 "attachment; filename=factura.html"})

@app.route('/group', methods=['GET','POST'])  
def group(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))


  
@app.route('/GenerarLetra', methods=['GET','POST'])
def GenerarLetra():
  consecutivo = int(request.form.get('txtConsecutivoActual'))
  factura = Factura.query.get(consecutivo)
  detalle = FacturaDetalle.query.filter(FacturaDetalle.facdet_Factura == factura.fac_numero).all()
  if(factura != None):
    cliente = Cliente.query.get(int(factura.fac_cliente))
    ValorDeLaFacturaEnLetras = num2words(factura.fac_Total, lang='es')
    hoy =  datetime.now(timezone('America/Bogota'))
    NumeroCommaSeparated = "{:,}".format(factura.fac_Total)

    path = 'C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/Letra.pdf'
    pagina = render_template("letra.html",detalle= detalle, cliente = cliente,factura = factura, hoy = hoy,ValorDeLaFacturaEnLetras = ValorDeLaFacturaEnLetras, NumeroCommaSeparated =  NumeroCommaSeparated)
    config = api.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

    pdf = api.from_string(pagina,False,configuration=config)
    
   
    return Response(
          pdf,
          mimetype="application/pdf",
          headers={"Content-disposition:":
                   "attachment; filename=factura.html"})  
  else:
     return jsonify("Factura inexistente") 

@app.route('/PonerPuntosDeMil', methods=['GET','POST'])
def PonerPuntosDeMil():
  Total = int(request.form.get('txtConsecutivoActual'))
  return jsonify(group(Total))


@app.route('/BuscarNumeroDeFacturas', methods=['GET','POST'])
def BuscarNumeroDeFacturas():
  Busqueda = Factura.query.filter(Factura.fac_cliente == int(request.form.get('txtCC_Nit'))).all()
  if Busqueda is None:
    return jsonify(0)
  else:
    return jsonify(len(Busqueda))

@app.route('/BuscarFacturaRelativo', methods=['GET','POST'])
def BBuscarFacturaRelativo():

 return jsonify(Factura.query.filter(Factura.fac_cliente == int(request.form.get('txtCC_Nit'))).all()[int(request.form.get('txtFacturaActual_Relacivo')) - 1].fac_numero)

@app.route('/PonerDiaDosDiasAparte', methods=['GET','POST'])
def PonerDiaDosDiasAparte():
  locale.setlocale(locale.LC_TIME, "vie")
  hoy = date.today()
  fac_eventoFecha = request.form.get('txtfechaEvento')
  
  if(date(int(fac_eventoFecha[6:10]), int(fac_eventoFecha[3:5]), int(fac_eventoFecha[0:2])) == hoy):
    DosDiasAtras = date(int(fac_eventoFecha[6:10]), int(fac_eventoFecha[3:5]), int(fac_eventoFecha[0:2]))  
  else:
    if hoy == date(int(fac_eventoFecha[6:10]), int(fac_eventoFecha[3:5]), int(fac_eventoFecha[0:2]))+ timedelta(days=1):
      DosDiasAtras = hoy
    else: 
      DosDiasAtras = date(int(fac_eventoFecha[6:10]), int(fac_eventoFecha[3:5]), int(fac_eventoFecha[0:2])) - timedelta(days=2)
  
  DosDiasAdelante = date(int(fac_eventoFecha[6:10]), int(fac_eventoFecha[3:5]), int(fac_eventoFecha[0:2])) + timedelta(days=2)
  if(hoy==date(int(fac_eventoFecha[6:10]), int(fac_eventoFecha[3:5]), int(fac_eventoFecha[0:2]))- timedelta(days=1)):
    DosDiasAtras = hoy

  if(DosDiasAdelante.strftime("%A") =="Sunday"):
     DosDiasAdelante = DosDiasAdelante + timedelta(days=1)

  listaDeFechas = [date(int(2017),int(7),int(20)),date(int(2017),int(8),int(7)),date(int(2017),int(8),int(21)),date(int(2017),int(10),int(16)), date(int(2017),int(11),int(6)),date(int(2017),int(11),int(13)),date(int(2017),int(12),int(8)),date(int(2017),int(12),int(25))]
  if date(DosDiasAdelante.year,DosDiasAdelante.month,DosDiasAdelante.day) in listaDeFechas:
    DosDiasAdelante = DosDiasAdelante + timedelta(days=1)

  return jsonify({'DosDiasAtras':DosDiasAtras,'DosDiasAtrasString':str(DosDiasAtras),'DosDiasDespues':DosDiasAdelante,'DosDiasDespuesString':str(DosDiasAdelante)})

@app.route('/BuscarReserva', methods=['GET','POST'])
def BuscarReserva():
  Entrega = request.form.get('txtfechaRecoger')
  Devolucion =  request.form.get('txtfechaDevolver')
  reservasProdcuto  = ReservasPrenda.query.filter(ReservasPrenda.ReservasPrenda_entrega > Entrega).filter(ReservasPrenda.ReservasPrenda_devolucion < Devolucion).all()
  if (reservasProdcuto == None):
    return jsonify("prenda no disponible en esta fecha, estara disponible el "+str(ReservasPrenda.ReservasPrenda_devolucion + timedelta(days=1)))

@app.route('/GenerarFactura', methods=['GET','POST'])
def GenerarFactura():
  factura = Factura.query.get(int(request.form.get('txtConsecutivoActual')))
  cliente = Cliente.query.get(int(factura.fac_cliente))
  path = 'C:/Users/Cidenet/Documents/VirutalEnvs/ikotia/ikotia/app/uploads/pdfs/Fffactura.pdf'
  medio = MedioConocio.query.get(int(cliente.cli_medioConocio))
  tipo = TipoPedido.query.get(int(factura.fac_tipoPedido))
  detalles = FacturaDetalle.query.filter(FacturaDetalle.facdet_Factura == factura.fac_numero).all()
  retefuente = request.form.get('txtRetefuente')
  facturaTotalConCommas = "{:,}".format(factura.fac_Total)
  pagina = render_template("facturaVdos.html",detalles= detalles,cliente = cliente,factura = factura,medio =medio.medio_nombre, tipo = tipo.pedi_nombre, retefuente =   retefuente, facturaTotalConCommas = facturaTotalConCommas)
  config = api.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

  pdf = api.from_string(pagina,False,configuration=config)
  
 
  return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-disposition:":
                 "attachment; filename=factura.html"})


@app.route('/FacturasDeCedula', methods=['GET','POST'])
def FacturasDeCedula():

  Busqueda = Factura.query.filter(Factura.fac_cliente == int(request.form.get('txtCC_Nit'))).all()
  if Busqueda is None:
    return jsonify(0)
  else:
    listFacturas = []
    listValor = []
    listFecha = []
    listSaldo = []
    for a in Busqueda:
      listFacturas.append(a.fac_numero)
      listValor.append(a.fac_Saldo)
      listFecha.append(a.fac_fechaFactura)
      listSaldo.append(a.fac_Saldo)
    return jsonify({'FacNumero': listFacturas,'Valor':listValor,'Fecha':listFecha, 'Saldo':listSaldo})
@app.route('/ReciboDeFactura', methods=['GET','POST'])
def ReciboDeFactura():

  Busqueda = Recibo.query.filter(Recibo.reci_Factura == int(request.form.get('txtConsecutivoActual'))).all()
  if Busqueda is None:
    return jsonify(0)
  else:
    listRecibo = []
    listValor = []
    listFecha = []
    listSaldo = []
    for r in Busqueda:
      listRecibo.append(r.reci_numero)
      listValor.append(r.reci_valor)
      listFecha.append(r.reci_fecha)
      listSaldo.append(r.reci_nuevoSaldo)
    return jsonify({'RecNumero': listRecibo,'Valor':listValor,'Fecha':listFecha, 'Saldo':listSaldo})

@app.route('/PonerMedidaYArreglo', methods=['GET','POST'])
def PonerMedidaYArreglo():
  InputMeter = str(request.form.get('InputMeter'))
  if InputMeter is None:
    InputMeter = " "
  LMLargoManga = request.form.get('LMLargoManga')
  if LMLargoManga is None:
    LMLargoManga = " "
  else:
    LMLargoManga = str(LMLargoManga)
  LMCintura = request.form.get('LMCintura')
  if LMCintura is None:
    LMCintura = " "
  else:
    LMCintura = str(LMCintura)
  LMLargoPantalon =  request.form.get('LMLargoPantalon')
  if LMLargoPantalon is None:
    LMLargoPantalon = " "
  else:
    LMLargoPantalon = str(LMLargoPantalon)
  HombreArreglo = request.form.get('HombreArreglo')
  if HombreArreglo is None:
    HombreArreglo = " "
  else:
    HombreArreglo = str(HombreArreglo)
  LFBusto = request.form.get('LFBusto')
  if LFBusto is None:
    LFBusto = " "
  else:
    LFBusto = str(LFBusto)
  LFCintura = request.form.get('LFCintura')
  if LFCintura is None:
    LFCintura = " "
  else:
    LFCintura = str(LFCintura)
  LFCadera = request.form.get('LFCadera') 
  if LFCadera is None:
    LFCadera = " "
  else:
    LFCadera = str(LFCadera)
  LFLargoTotal = request.form.get('LFLargoTotal')
  if LFLargoTotal is None:
    LFLargoTotal = " "
  else:
    LFLargoTotal = str(LFLargoTotal)
  MujerArreglo = request.form.get('MujerArreglo')
  if MujerArreglo is None:
    MujerArreglo = " "
  else:
    MujerArreglo = str(MujerArreglo)

  if LMLargoManga:
    StringMasculino = "Largo manga:"+LMLargoManga+",Cintura:"+LMCintura+",Largo pantalon:"+LMLargoPantalon+",Arreglo:"+HombreArreglo
    return jsonify({'datus':StringMasculino,'input':InputMeter})
  if LMCintura:
    StringMasculino = "Largo manga:"+LMLargoManga+",Cintura:"+LMCintura+",Largo pantalon:"+LMLargoPantalon+",Arreglo:"+HombreArreglo
    return jsonify({'datus':StringMasculino,'input':InputMeter})
  if LMLargoPantalon:
    StringMasculino = "Largo manga:"+LMLargoManga+",Cintura:"+LMCintura+",Largo pantalon:"+LMLargoPantalon+",Arreglo:"+HombreArreglo
    return jsonify({'datus':StringMasculino,'input':InputMeter})
  if HombreArreglo:
    StringMasculino = "Largo manga:"+LMLargoManga+",Cintura:"+LMCintura+",Largo pantalon:"+LMLargoPantalon+",Arreglo:"+HombreArreglo
    return jsonify({'datus':StringMasculino,'input':InputMeter})
  if LFBusto:
    StringFemenino = "Busto:"+LFBusto+",Cintura:"+LFCintura+",Cadera:"+LFCadera+",Largo total:"+LFLargoTotal+",Arreglo:"+MujerArreglo
    return jsonify({'datus':StringFemenino,'input':InputMeter}) 
  if LFCintura:
    StringFemenino = "Busto:"+LFBusto+",Cintura:"+LFCintura+",Cadera:"+LFCadera+",Largo total:"+LFLargoTotal+",Arreglo:"+MujerArreglo
    return jsonify({'datus':StringFemenino,'input':InputMeter})
  if LFCadera:
    StringFemenino = "Busto:"+LFBusto+",Cintura:"+LFCintura+",Cadera:"+LFCadera+",Largo total:"+LFLargoTotal+",Arreglo:"+MujerArreglo
    return jsonify({'datus':StringFemenino,'input':InputMeter})
  if LFLargoTotal:
    StringFemenino = "Busto:"+LFBusto+",Cintura:"+LFCintura+",Cadera:"+LFCadera+",Largo total:"+LFLargoTotal+",Arreglo:"+MujerArreglo
    return jsonify({'datus':StringFemenino,'input':InputMeter})
  if MujerArreglo:
    StringFemenino = "Busto:"+LFBusto+",Cintura:"+LFCintura+",Cadera:"+LFCadera+",Largo total:"+LFLargoTotal+",Arreglo:"+MujerArreglo
    return jsonify({'datus':StringFemenino,'input':InputMeter})  

@app.route('/AlterarPrecioTreinta', methods=['GET','POST'])
def AlterarPrecioTreinta():
  #knout out
  PrecioReferencia = CantidadPrenda.query.get(request.form.get('ReferenciaPrenda')).cantidadPrenda_ValorReferencia
  precioAlterado = request.form.get('txtValorReferencia')

  #if(int(str(request.form.get('txtValorReferencia')))) ==
  if(str(request.form.get('PasswordSAVED')) == "siEra"):
    if(precioAlterado == None):
      return jsonify({'precio':0,'respuesta':'cambio permitido','input':request.form.get('w')}) 
    else:
      return jsonify({'precio':precioAlterado,'respuesta':'cambio permitido','input':request.form.get('w')})  
  else:
    if((int(precioAlterado) +(0.30*PrecioReferencia))<PrecioReferencia and str(current_user.usu_login) != "john"):
      return jsonify({'precio':PrecioReferencia,'respuesta':'excedio el limite de 30%','input':request.form.get('w')})
    else:
      return jsonify({'precio':precioAlterado,'respuesta':'cambio permitido','input':request.form.get('w')})

@app.route('/VerificarFestivo', methods=['GET','POST'])
def VerificarFestivo():
  ListaDeFestivos = [date(2007,7,20),date(2007,8,7),date(2007,8,21),date(2007,10,16),date(2007,11,6),date(2007,11,13),date(2007,12,8),date(2007,12,25)]
  fac_ReclamarMercanciaFecha = str(request.form.get('fecha'))
  if(fac_ReclamarMercanciaFecha[0:3] == "201" ):
    fac_ReclamarMercanciaFecha=date(int(fac_ReclamarMercanciaFecha[0:4]),int(fac_ReclamarMercanciaFecha[5:7]),int(fac_ReclamarMercanciaFecha[8:10]))
  else:
    fac_ReclamarMercanciaFecha= date(int(fac_ReclamarMercanciaFecha[6:10]),int(fac_ReclamarMercanciaFecha[3:5]), int(fac_ReclamarMercanciaFecha[0:2]))
  if fac_ReclamarMercanciaFecha in ListaDeFestivos:
    return jsonify("este dia es festivo")
  else:
    return jsonify("1")

@app.route('/ObtenerTotal', methods=['GET','POST'])
def ObtenerTotal():
  total = 0
  for a in range(len(request.form.getlist('txtValorReferenciaArray[]',type= int))):
    total = total + a

  return jsonify(total)
  
@app.route('/AutomatizarPrenda', methods=['GET','POST'])
def AutomatizarPrenda(): 
  descripcion = CantidadPrenda.query.filter(CantidadPrenda.cantidadPrenda_id == request.form.get('txtReferencia')).all()[0].cantidadPrenda_descripcion
  accesorios = CantidadPrenda.query.filter(CantidadPrenda.cantidadPrenda_id == request.form.get('txtReferencia')).all()[0].cantidadPrenda_Accesorios
  valor = CantidadPrenda.query.filter(CantidadPrenda.cantidadPrenda_id == request.form.get('txtReferencia')).all()[0].cantidadPrenda_ValorReferencia
  sexo = CantidadPrenda.query.filter(CantidadPrenda.cantidadPrenda_id == request.form.get('txtReferencia')).all()[0].SexoLinea
  fac_DevolverMercanciaFecha = str(request.form.get('txtfechaDevolver'))
  fac_DevolverMercanciaFechaExacto = str(request.form.get('txtfechaDevolver'))
  fac_ReclamarMercanciaFecha = str(request.form.get('txtfechaRecoger'))
  fac_ReclamarMercanciaFechaExacto = str(request.form.get('txtfechaRecoger'))
  hoy = datetime.now()
  hoy = date(hoy.year, hoy.month, hoy.day)
  reservaResulT = "no"
  ListaDeRangos =[]
  fecha_a_reservarDosDiasLIST =[]
  fecha_a_reservarMismoDiaLIST =[]
  fecha_a_reservarCORAZONLIST =[]
  fecha_a_reservarOUTSIDELIST =[]
  FINALlist = []
  
  if(fac_DevolverMercanciaFecha[0:3] == "201" ):
    fac_DevolverMercanciaFecha=date(int(fac_DevolverMercanciaFecha[0:4]),int(fac_DevolverMercanciaFecha[5:7]),int(fac_DevolverMercanciaFecha[8:10]))+timedelta(days=2)
    fac_DevolverMercanciaFechaExacto= date(int(fac_DevolverMercanciaFechaExacto[0:4]),int(fac_DevolverMercanciaFechaExacto[5:7]),int(fac_DevolverMercanciaFechaExacto[8:10]))
  else:
    fac_DevolverMercanciaFecha= date(int(fac_DevolverMercanciaFecha[6:10]), int(fac_DevolverMercanciaFecha[3:5]), int(fac_DevolverMercanciaFecha[0:2]))+timedelta(days=2)
    fac_DevolverMercanciaFechaExacto= date(int(fac_DevolverMercanciaFechaExacto[6:10]), int(fac_DevolverMercanciaFechaExacto[3:5]), int(fac_DevolverMercanciaFechaExacto[0:2]))
  if(fac_ReclamarMercanciaFecha[0:3] == "201"):
    fac_ReclamarMercanciaFecha= date(int(fac_ReclamarMercanciaFecha[0:4]),int(fac_ReclamarMercanciaFecha[5:7]),int(fac_ReclamarMercanciaFecha[8:10]))-timedelta(days=2)
    fac_ReclamarMercanciaFechaExacto= date(int(fac_ReclamarMercanciaFechaExacto[0:4]),int(fac_ReclamarMercanciaFechaExacto[5:7]),int(fac_ReclamarMercanciaFechaExacto[8:10]))
  else:
    fac_ReclamarMercanciaFecha= date(int(fac_ReclamarMercanciaFecha[6:10]), int(fac_ReclamarMercanciaFecha[3:5]), int(fac_ReclamarMercanciaFecha[0:2]))-timedelta(days=2)
    fac_ReclamarMercanciaFechaExacto= date(int(fac_ReclamarMercanciaFechaExacto[6:10]), int(fac_ReclamarMercanciaFechaExacto[3:5]), int(fac_ReclamarMercanciaFechaExacto[0:2]))
  for rara in  FechaEntreFechas(fac_ReclamarMercanciaFecha, fac_DevolverMercanciaFecha, timedelta(days=1)):
    fecha_a_reservarDosDiasLIST.append(rara)


  reservas = ReservasPrenda.query.filter(ReservasPrenda.ReservasPrenda_entrega_nombre_talla_color == int(request.form.get('txtReferencia'))).all()
  #primero reservemos
  for reser in reservas:
    if reser.ReservasPrenda_devolucion > hoy:
      ListaDeRangos.append(FechaEntreFechas(reser.ReservasPrenda_entrega,reser.ReservasPrenda_devolucion,timedelta(days=1)))
      for lista in ListaDeRangos:
        if (bool(set(fecha_a_reservarDosDiasLIST) & set(lista))):#hasta aqui funciona perfecto ahora necesito saber 
          for last in  ReservasPrenda.query.filter( ReservasPrenda.ReservasPrenda_entrega_nombre_talla_color == int(request.form.get('txtReferencia'))).filter(ReservasPrenda.ReservasPrenda_devolucion > hoy).all():
            FINALlist.append(FechaEntreFechas(last.ReservasPrenda_entrega, last.ReservasPrenda_devolucion, timedelta(days=1)))
            for fechaFin in FINALlist:
              if (bool(set(fecha_a_reservarDosDiasLIST) & set(fechaFin))):
                reservaResulT = "Reservado, coincide con la factura: "+str(last.ReservasPrenda_factura)+"  cuyo dia de devolucion es: "+str(last.ReservasPrenda_devolucion)
                break
          #for heart in  FechaEntreFechas(fac_ReclamarMercanciaFechaExacto, fac_DevolverMercanciaFechaExacto, timedelta(days=1)):
            
  
  return jsonify({"descripcion": descripcion ,"accesorios": accesorios,"valor_sugerido": valor,"sexo": sexo,"fecha_prueba1":fac_ReclamarMercanciaFecha,"fecha_prueba2":fac_DevolverMercanciaFecha,"reservaResulT":reservaResulT})

@app.route('/ValorTotalEnLetras', methods=['GET','POST'])
def ValorTotalEnLetras(): 
  total = 0
  for a in request.form.getlist('txtValoresReferenciaArray[]',type= str):
    if (a.isdigit()):
      total = total + int(a)
  return jsonify({"letras":num2words(total, lang='es'),"numeros":total})
  
@app.route('/QuitarHoraReservada', methods=['GET','POST'])
def QuitarHoraReservada():


  fac_ReclamarMercanciaFecha = str(request.form.get('txtfechaRecoger'))

  ListaDeHoras = []
  
  if(fac_ReclamarMercanciaFecha[0:3] == "201" ):
    if(int(fac_ReclamarMercanciaFecha[5:7]) > 9):
      tempo_rada = "alta"
    else:
      tempo_rada = "baja"
    fac_ReclamarMercanciaFecha=date(int(fac_ReclamarMercanciaFecha[0:4]),int(fac_ReclamarMercanciaFecha[5:7]),int(fac_ReclamarMercanciaFecha[8:10]))
  else:
    if(int(fac_ReclamarMercanciaFecha[3:5]) > 9):
      tempo_rada = "alta"
    else:
      tempo_rada = "baja"
    fac_ReclamarMercanciaFecha = date(int(fac_ReclamarMercanciaFecha[6:10]),int(fac_ReclamarMercanciaFecha[3:5]),int(fac_ReclercanciaFecha[0:2]))


  if HoraRecogidaReserva.query.filter(HoraRecogidaReserva.HoraReco_fechaSlash == fac_ReclamarMercanciaFecha) is not None:
    for hour in range(len(HoraRecogidaReserva.query.filter(HoraRecogidaReserva.HoraReco_fechaSlash == fac_ReclamarMercanciaFecha).all())):
      ListaDeHoras.append(HoraRecogidaReserva.query.filter(HoraRecogidaReserva.HoraReco_fechaSlash == fac_ReclamarMercanciaFecha).all()[hour].HoraReco_hora)
    return jsonify({'lista':ListaDeHoras,'tempo':tempo_rada})

  #  #https://stackoverflow.com/questions/7697936/jquery-show-hide-options-from-one-select-drop-down-when-option-on-other-select


@app.route('/VendedorIngresandoPassWord', methods=['GET','POST'])
def VendedorIngresandoPassWord():
  PassSkill.query.filter(PassSkill.PassSKill_id == 1).update({PassSkill.PassSKill_text : request.form.get('PasswordSkillOwner')})
  db.session.commit() 
  return jsonify ("contraseña cambiada") 

@app.route('/CambiarContraseñaDeSistema', methods=['GET','POST'])
def CambiarContraseñaDeSistema():
  lista = PassSkill.query.get(1)
  atributo = lista.PassSKill_text
  if (atributo == str(request.form.get('txtPassEnviado'))):
    return jsonify("siEra")
  else:
    return jsonify("nuu")
@app.route('/MostrarBotonCambiadorDePass', methods=['GET','POST'])
def MostrarBotonCambiadorDePass():
  if(str(current_user.usu_login) != "john"):
    return jsonify("mostrar")
  else:
    return jsonify("cambiar")

@app.route('/PonerOtros', methods=['GET','POST'])
def PonerOtros():
  if(str(request.form.get('opcionOtru')) == "ciudad"):
    newcity = Ciudad(str(request.form.get('CiudadOtro')),1,1,1,str(current_user),str(current_user))
    db.session.add(newcity)
    db.session.commit() 

  if(str(request.form.get('opcionOtru')) == "MedioComuni"):
    comuni = MedioConocio(request.form.get('Medio_comunicacionOtro'))
    db.session.add(comuni)
    db.session.commit() 
    
  if(str(request.form.get('opcionOtru')) == "TipoEvento"):
    eeeve = Evento(request.form.get('Tipo_EventoOtro'))
    db.session.add(eeeve)
    db.session.commit()

@app.route('/UncheckDaPrice', methods=['GET','POST'])
def UncheckDaPrice():
  return jsonify(CantidadPrenda.query.filter(CantidadPrenda.cantidadPrenda_id == request.form.get('ReferenciaPrenda')).all()[0].cantidadPrenda_ValorReferencia)
  #reverificarReserva

@app.route('/RevisarQueFalto', methods=['GET','POST'])
def RevisarQueFalto():
  FaltaronDaList = []
  FaltaronDaListNames = []
  FaltaronDaList.append("le faltaron estos campos")
  FaltaronDaListNames.append("le faltaron estos campos")
  nombre = request.form.get('txtNonmbreCliente')
  if nombre:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("nombre")
  else:
    FaltaronDaList.append("no")
  CcNit = request.form.get("txtCC_Nit")
  if CcNit:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  DiaCumpleaños = request.form.get("txtDiaCumpleaños")
  if DiaCumpleaños:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  MesCumpleaños = request.form.get('txtMesCumpleaños')#[]
  if MesCumpleaños:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  TelFijo = request.form.get("txtTelefonoFijo")
  if TelFijo:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  Ext = request.form.get("Ext")
  if Ext:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  TelFijoOficina = request.form.get("txtTelefonoFijoOficina")
  ExtOficina = request.form.get("ExtOficina")
  Celular = request.form.get("txtCelular")
  if Celular:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  Email = request.form.get('txtEmail')#[]
  if Email:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  Direccion = request.form.get('txtDireccion')#[]
  if Direccion:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  if request.form.get('txtMunicipio'):
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  if(str(request.form.get('txtMunicipio')).isdigit()):
    Municipio = request.form.get('txtMunicipio')
  else:
    Municipio = Ciudad.query.filter(Ciudad.ciu_nombre == str(request.form.get('txtMunicipio'))).all()[0].ciu_id
  Barrio = request.form.get('txtBarrio')#[]
  if(str(request.form.get('txtMedioConocio')).isdigit()):
    MedioConocio = request.form.get('txtMedioConocio')
  else:
    MedioConocio = MedioConocio.query.filter(MedioConocio.medio_nombre == str(request.form.get('txtMedioConocio'))).all()[0].medio_id
  if Barrio:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  Poblacion = request.form.get('txtPedPoblacion')
  if Poblacion:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  #
  #
  #
  TipoPedido = request.form.get('txtTipoPedido')
  if(str(request.form.get('txtTipoEvento')).isdigit()):
    TipoEvento = request.form.get('txtTipoEvento')
  else:
    TipoEvento = Evento.query.filter(Evento.eve_nombre == str(request.form.get('txtTipoEvento'))).all()[0].eve_id
  if TipoPedido:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  if TipoEvento:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
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
  Abono =  request.form.get('txtAbono')
  Retefuente = request.form.get('txtRetefuente')
  ReferenciaNombre = request.form.get('txtReferenciaNombre')#[]
  ReferenciaCelular = request.form.get('txtReferenciaCelular')#[]
  ReferenciaTelefono = request.form.get('txtReferenciaTelefono')#[]
  Nota = request.form.get('txtNota')#[]
  #
  ConsecutivoManual = request.form.get('txtConsecutivoManual')#[]z
  Consecutivo = request.form.get('txtConsecutivo')#[]z
  ConsecutivoActual = request.form.get('txtConsecutivoActual')
  hoy = "{:%d.%m.%Y}".format(datetime.now())
  fac_fechaFactura = hoy
  fac_horasCadaReclamarMH = request.form.get('txtHoraReclamarA')
  fac_horasReclamarCadaH = request.form.get('txtHoraReclamarB')
  fac_horasDevolverCadaH  = request.form.get('txtHoraDevolverB')
  fac_horasCadaDevolverMH = request.form.get('txtHoraDevolverA')
  eventoFecha = str(request.form.get('txtfechaEvento'))
  Retefuente = request.form.get('txtRetefuente')
  fac_eventoFecha = str(request.form.get('txtfechaEvento'))
  if fac_eventoFecha:
    FaltaronDaList.append("si")
    FaltaronDaListNames.append("txtCC_Nit")
  else:
    FaltaronDaList.append("no")
  fac_ReclamarMercanciaFecha = str(request.form.get('txtfechaRecoger'))
  fac_DevolverMercanciaFecha  = str(request.form.get('txtfechaDevolver'))
  fac_horasDevolverCadaH = request.form.get('txtHoraDevolverB')
  fac_horasReclamarCadaH = request.form.get('txtHoraReclamarB')
  fac_horasCadaDevolverMH   = request.form.get('txtHoraDevolverA')
  fac_horasCadaReclamarMH = request.form.get('txtHoraReclamarA')
  fac_CantidadLLeva1 = request.form.get('cantidadRealPrenda1')
  fac_CantidadLLeva2 = request.form.get('cantidadRealPrenda2')
  fac_CantidadLLeva3 = request.form.get('cantidadRealPrenda3')
  fac_CantidadLLeva4 = request.form.get('cantidadRealPrenda4')

  return jsonisy({'FaltaronDaList':FaltaronDaList,'FaltaronDaListNames':FaltaronDaListNames})

