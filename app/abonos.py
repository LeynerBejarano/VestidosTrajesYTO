import os
from app import app, db, mail_ext
from app.utils import numero_a_moneda, numero_a_letras
from xhtml2pdf import pisa
from io import BytesIO
from flask import redirect, render_template, flash, request, jsonify, send_from_directory
from flask.ext.login import login_required, current_user
from flask.ext.wtf import Form
from flask.ext.mail import Mail, Message
from wtforms import StringField, DecimalField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, InputRequired, Required
from wtforms.fields.html5 import DateField
from app.model.ciudad import Ciudad
from app.model.prenda import Prenda
from app.model.despacho import Despacho
from app.model.pedido import Pedido
from app.model.accesorio import Accesorio
from app.model.det_pedido import Det_pedido
from app.model.det_despacho import Det_despacho
from app.model.empresa import Empresa
from app.model.institucion import Institucion
from app.model.jornada import Jornada
from app.model.nivele import Nivele
from app.model.cliente import Cliente
from app.model.abono import Abono
from app.model.tipo_pago import Tipo_pago
from app.utils import numero_a_letras

class Input_abo(Form):
    pedido = StringField('Pedido<span class="obligatorio">*</span>', validators=[DataRequired()])
    valor = DecimalField('Valor<span class="obligatorio">*</span>', validators = [DataRequired()])
    tipo = SelectField('Tipo de pago<span class="obligatorio">*</span>', validators=[DataRequired()], coerce = int)
    fecha = DateField('Fecha de pago', validators=[Optional()])     
    observacion = TextAreaField('Observaciones')

@app.route('/abonos', methods=['GET', 'POST'])
@login_required
def abonos():
    datos = {'title' : 'Facturación Losdelastogas'}
    form = Input_abo()
    form.tipo.choices = [(t.tip_id, t.tip_nombre) for t in Tipo_pago.query.all()]
    pedido = request.args.get('pedido')
    if pedido:
        form.pedido.data = pedido
    if form.validate_on_submit():
        if not Pedido.query.get(form.pedido.data):
            flash(u'Error: no existe el pedido ingresado', 'danger')
            return redirect('abonos')
        new_abono = Abono(form.pedido.data, form.valor.data, form.tipo.data, form.fecha.data, form.observacion.data, current_user.usu_login, None)
        db.session.add(new_abono)
        db.session.commit()
        abonoTotal = 0
        update_pedido_abo(form.pedido.data)
        try:
            filename = send_pdf(form.pedido.data)
            filenames = [filename]        
            consecutivo = {'pedido': form.pedido.data, 'abono': new_abono.abo_id}
            label = {'concepto': 'Abono', 'accion': 'ingresado'}
            return render_template("success.html", datos = datos, consecutivo = consecutivo, filenames = filenames, label = label)
        except Exception as e:
            flash(u'Abono guardado con error al enviar el E-mail: Revisar si se ha cambiado la contraseña del correo recientemente o si se bloqueó la salida del correo por seguridad.', 'warning')
            return redirect('abonos')   
    return render_template("abonos.html", datos = datos, form = form)

@app.route('/_exportar_abonos', methods=['GET', 'POST'])
@login_required
def exportar_abonos():
  id = request.args.get('id')
  pedido = Pedido.query.get(id)
  if pedido:
    abonos = Abono.query.filter(Abono.abo_pedido == pedido.ped_numero)
    file = 'informe_abonos.pdf'
    total = 0
    det_abono = []
    for abono in abonos:
      total += abono.abo_valor
      valor = format(float(abono.abo_valor), ',.2f')
      fecha_ingreso = abono.abo_fecha_mod.strftime('%b-%d-%Y')
      if abono.abo_fecha:
        fecha_pago = abono.abo_fecha.strftime('%b-%d-%Y')
      else:
        fecha_pago = None
      det_abono.append([abono.abo_id, valor, fecha_pago, fecha_ingreso])
    detalle = Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero, Det_pedido.det_clase == pedido.ped_principal).first()
    if not detalle:
      detalle = Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero).first()
    valorPedido = detalle.det_pedida * pedido.ped_val_unitario
    saldoPedido = valorPedido - total
    saldoPedido = format(float(saldoPedido),',.2f')
    det_pedido = {'saldo': saldoPedido}

    create_pdf(render_template("informe_abono.html", pedido = pedido, det_pedido = det_pedido, total = total, det_abono = det_abono), file)
    return jsonify(flag = True)
  else:
    return jsonify(flag = False)

@app.route('/recibo_blanco', methods=['GET', 'POST'])
@login_required
def recibo_blanco():
  empresa = Empresa.query.get(98533266)
  filename = 'recibo_abono.pdf'
  create_pdf(render_template("recibo_abono.html", empresa = empresa), filename)
  return send_from_directory(app.config['UPLOAD_FOLDER'] + 'pdf/', filename, as_attachment=True)

@app.route('/_formatear_valor')
def formatear_valor():
  valor = request.args.get('valor')
  try:
    moneda = format(float(valor),',.2f')
    letra = numero_a_moneda(float(valor))
  except Exception:
    moneda = 'valor erroneo'
    letra = 'Valor erroneo'
  return jsonify(moneda = moneda, letra = letra)

@app.route('/_cargar_abonos')
def cargar_abonos():
    id = request.args.get('id')
    abonos = [abono.serialize for abono in Abono.query.filter(Abono.abo_pedido == id)]
    for abono in abonos:
      abono['valor'] = '$' + format(float(abono['valor']), ',.2f')
      abono['tipo'] = Tipo_pago.query.get(abono['tipo']).tip_nombre
    return jsonify(abonos = abonos)


def update_pedido_abo(pedido):
    abonoTotal = get_abono_total(pedido)
    Pedido.query.filter(Pedido.ped_numero == pedido).update({Pedido.ped_abono: abonoTotal}, synchronize_session=False)
    db.session.commit()

def get_abono_total(pedido):
    abonos = Abono.query.filter(Abono.abo_pedido == pedido).all()
    abonoTotal = 0
    for abono in abonos:
        abonoTotal += abono.abo_valor
    return abonoTotal

def gen_pdf(idPedido, file):
    pedido = Pedido.query.get(idPedido)
    cliente = Cliente.query.get(pedido.ped_cliente)
    institucion = Institucion.query.get(pedido.ped_institucion)
    abono = Abono.query.filter(Abono.abo_pedido == idPedido).order_by(Abono.abo_fecha_mod.desc()).first()
    empresa = Empresa.query.get(pedido.ped_empresa)
    detalle = Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero, Det_pedido.det_clase == pedido.ped_principal).first()
    if not detalle:
      detalle = Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero).first()
    valorPedido = detalle.det_pedida * pedido.ped_val_unitario
    abonoTotal = get_abono_total(idPedido)
    saldoPedido = valorPedido - abonoTotal
    saldoPedido = format(float(saldoPedido),',.2f')
    abonoTexto = numero_a_moneda(abono.abo_valor)
    det_pedido = {'ciudad': 'Medellín', 'fecha': abono.abo_fecha_mod.strftime('%b-%d-%Y'), 'abono': abonoTotal, 'cantidad': detalle.det_pedida, 'valor': format(float(valorPedido),',.2f'), 'saldo': saldoPedido, 'abonoTexto': abonoTexto, 'valor_unitario': format(float(pedido.ped_val_unitario), ',.2f'), 'jornada': Jornada.query.get(pedido.ped_jornada).jor_nombre, 'nivel': Nivele.query.get(pedido.ped_nivel).niv_nombre}

    despacho = Despacho.query.filter(Despacho.des_pedido == pedido.ped_numero, Despacho.des_prestamo == 5).first()
    det_despacho = None
    if despacho:
      cantidad = 0
      for detalle in Det_despacho.query.filter(Det_despacho.tal_despacho == despacho.des_id):
        cantidad += detalle.tal_cantidad
      valorDespacho = cantidad * pedido.ped_val_unitario
      saldoDespacho = valorDespacho - abonoTotal
      det_despacho = {'cantidad': cantidad, 'valor': format(float(valorDespacho),',.2f'), 'saldo': format(float(saldoDespacho),',.2f')}
    fecha = None
    if abono.abo_fecha:
        fecha = abono.abo_fecha.strftime('%b-%d-%Y')
    det_abono = {'valor': format(float(abono.abo_valor), ',.2f'), 'fecha': fecha, 'tipo': Tipo_pago.query.get(abono.abo_tipo).tip_nombre}
    pdf = create_pdf(render_template("recibo_abono.html", pedido = pedido, det_pedido = det_pedido, despacho = despacho, det_despacho = det_despacho, abono = abono, det_abono = det_abono, institucion = institucion, empresa = empresa, cliente = cliente), file)
    return pdf

def create_pdf(pdf_data, filename):
    pdf = open(os.path.join(app.config['UPLOAD_FOLDER'], 'pdf/' + filename), 'wb')
    pisa.CreatePDF(BytesIO(pdf_data.encode('utf-8')), pdf)
    pdf.close() 
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(pdf_data.encode('utf-8')), pdf)
    return pdf

def send_pdf(id):
  pedido = Pedido.query.get(id)
  abono = Abono.query.filter(Abono.abo_pedido == pedido.ped_numero).order_by(Abono.abo_fecha_mod.desc()).first()
  cliente = Cliente.query.get(pedido.ped_cliente)
  institucion = Institucion.query.get(pedido.ped_institucion)
  subject = "Abono No. " + str(abono.abo_id) + " Pedido No. " + str(pedido.ped_numero) + " " + abono.abo_fecha_mod.strftime('%b-%d-%Y %H:%M %p')
  receiver1 = cliente.cli_email
  # receiver2 = 'losdelastogas@gmail.com'
  msg = Message(subject=subject, sender='losdelastogas@gmail.com', recipients=[receiver1])
  msg.body = "Pedido No. " + str(pedido.ped_numero) + "\nInstitución: " + institucion.ins_nombre + " NIT: " + str(institucion.ins_nit) + "\nEncargado: " + cliente.cli_nombre + " " + cliente.cli_apellido + " Identificación: " + str(cliente.cli_identificacion)
  file = 'abono.pdf'
  pdf = gen_pdf(id, file)
  # pdf = open(os.path.join(app.config['UPLOAD_FOLDER'], 'pdf/' + file), 'r')
  msg.attach(file, "application/pdf", pdf.getvalue())
  # pdf.close()
  mail_ext.send(msg)
  return file


