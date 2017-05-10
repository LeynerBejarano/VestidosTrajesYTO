                        
                         
                         
                         
                         
                         
                         
                         

def date_format(date):
  try:
    return date.strftime('%b-%d-%Y')
  except Exception:
    return None

def notificar_ciudad(ciudad):
  subject = "Nueva ciudad ingresada al sistema"
  receiver = "cardonajohn@hotmail.com"
  msg = Message(subject=subject, sender='losdelastogas@gmail.com', recipients=[receiver])
  msg.html = "Se ha ingresado la ciudad <strong>" + ciudad + "</strong> al sistema de facturacion. Puede modificar su nombre ingresando al enlace: Datos->municipios"
  mail_ext.send(msg)  

def notificar_valor_menor(antiguo, nuevo, usuario, pedido):
  subject = "ALERTA: Valor unitario modificado"
  receiver = "cardonajohn@hotmail.com"
  msg = Message(subject=subject, sender='losdelastogas@gmail.com', recipients=[receiver])
  msg.html = "El usuario <strong>" + usuario + "</strong> ha modificado el valor unitario del pedido No. <strong>" + str(pedido) + "</strong>. Teniendo el pedido, un valor anterior de <strong>" + format(float(antiguo),',.2f') + "</strong>, y un nuevo valor de <strong>" + format(float(nuevo),',.2f') + "</strong>."
  mail_ext.send(msg)  

def notificar_valor_sugerido(sugerido, valor, usuario, pedido):
  subject = "ALERTA: Valor unitario menor al sugerido"
  receiver = "cardonajohn@hotmail.com"
  msg = Message(subject=subject, sender='losdelastogas@gmail.com', recipients=[receiver])
  msg.html = "El usuario <strong>" + usuario + "</strong> ha ingresado el valor unitario del pedido No. <strong>" + str(pedido) + "</strong> menor al 70 por ciento del valor sugerido.\nValor Ingresado: <strong>" + format(float(valor),',.2f') + "</strong>\nValor sugerido: <strong>" + format(float(sugerido),',.2f') + "</strong>."
  mail_ext.send(msg)  


@app.route('/_cargar_cliente')
def cargar_cliente():
  identificacion = request.args.get('id')
  cliente = Cliente.query.get(identificacion)
  return jsonify(nombre = cliente.cli_nombre, apellido = cliente.cli_apellido, cargo = cliente.cli_cargo, celular = cliente.cli_celular, email = cliente.cli_email, direccion = cliente.cli_direccion, telefono = cliente.cli_telefono, extension = cliente.cli_extension, municipio = cliente.cli_ciudad, barrio = cliente.cli_barrio, mes = cliente.cli_nacido_mes, dia = cliente.cli_nacido_dia)

@app.route('/_cargar_institucion')
def cargar_institucion():
  nit = request.args.get('nit')
  ins = Institucion.query.get(nit)
  if ins:
    return jsonify(nombre = ins.ins_nombre, nit = int(ins.ins_nit), ciudad = ins.ins_ciudad)
  else:
    return jsonify(None)


@app.route('/_cargar_area')
def cargar_area():
  id = request.args.get('id')
  ciudad = Ciudad.query.filter(Ciudad.ciu_id == id).first()
  if ciudad:
    if ciudad.ciu_metropol == 0:
      precio = 5000
    else:
      precio = 0
    return jsonify(area = ciudad.ciu_metropol, precio = precio)
  else:
    return jsonify(area = -1)

@app.route('/_cargar_temporada')
def cargar_temporada():
  fecha = request.args.get('fecha')
  temporada = ""
  if fecha:
    fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    temporada = get_temporada(fecha)
  return jsonify(temporada = temporada)


@app.route('/_cargar_estilos')
def cargar_estilos():
  clase = request.args.get('clase')
  color = request.args.get('color')
  prendas = Prenda.query.filter(Prenda.pre_clase == clase, Prenda.pre_color == color).group_by(Prenda.pre_estilo)
  accesorios = Accesorio.query.filter(Accesorio.acc_clase == clase, Accesorio.acc_color == color).group_by(Accesorio.acc_estilo)

  if prendas.all():
    estilos = [(prenda.pre_estilo, Estilo.query.get(prenda.pre_estilo).est_nombre) for prenda in prendas]
  elif accesorios.all():
    estilos = [(accesorio.acc_estilo, Estilo.query.get(accesorio.acc_estilo).est_nombre) for accesorio in accesorios]
  else:
    estilos = []
  return jsonify(estilos = estilos)

@app.route('/_cargar_dias')
def cargar_dias():
  ### Dias del mes dado, de un año no bisiesto (2015)
  mes = request.args.get('mes')
  choices = [(i + 1, str(i + 1)) for i in range(monthrange(2015,int(mes))[1])]
  return jsonify(choices = choices)



@app.route('/_cargar_val_unitario')
def cargar_val_unitario():
  clase = request.args.get('clase')
  color = request.args.get('color')
  estilo = request.args.get('estilo')
  prenda = Prenda.query.filter(Prenda.pre_clase == clase, Prenda.pre_color == color, Prenda.pre_estilo == estilo).first()
  if prenda:
    val_unitario = prenda.pre_val_unitario
    return jsonify(val_unitario = float(val_unitario))

  accesorio = Accesorio.query.filter(Accesorio.acc_clase == clase, Accesorio.acc_color == color, Accesorio.acc_estilo == estilo).first()
  if accesorio:
    val_unitario = accesorio.acc_val_unitario
    return jsonify(val_unitario = float(val_unitario))

  return jsonify(val_unitario = 0)

@app.route('/_cargar_val_entrega')
def cargar_val_entrega():
  id = request.args.get('id')
  print(id)
  if id and int(id) < 2:
    entrega = Entrega.query.get(1)
  else:
    entrega = Entrega.query.get(2)
  return jsonify(val_unitario = float(entrega.ent_val_unitario))

@app.route('/_cargar_val_estola')
def cargar_val_estola():
  id = request.args.get('id')
  tipo_estola = Tipo_estola.query.get(id)
  return jsonify(val_unitario = float(tipo_estola.tes_val_unitario))

@app.route('/_cargar_tipo_orden')
def cargar_tipo_orden():
  id = request.args.get('id')
  tipo_orden = Tipo_orden.query.get(id)
  return jsonify(tipo = tipo_orden.tip_tipo)

@app.route('/_cargar_disponible')
def cargar_disponible():
  fecha = request.args.get('fecha')
  color = request.args.get('color')
  estilo = request.args.get('estilo')
  clase = request.args.get('clase')
  total = 0
  if Prenda.query.filter(Prenda.pre_clase == clase).first():
    if color:
      if estilo:
        total = float(Prenda.query.filter(Prenda.pre_clase == clase, Prenda.pre_color == color, Prenda.pre_estilo == estilo).with_entities(func.sum(Prenda.pre_cantidad).label('total')).first().total)
      else:
        total = float(Prenda.query.filter(Prenda.pre_clase == clase, Prenda.pre_color == color).with_entities(func.sum(Prenda.pre_cantidad).label('total')).first().total)
    else:
      total = float(Prenda.query.filter(Prenda.pre_clase == clase).with_entities(func.sum(Prenda.pre_cantidad).label('total')).first().total)

  elif Accesorio.query.filter(Accesorio.acc_clase == clase).first():
    if color:
      if estilo:
        total = float(Accesorio.query.filter(Accesorio.acc_clase == clase, Accesorio.acc_color == color, Accesorio.acc_estilo == estilo).with_entities(func.sum(Accesorio.acc_cantidad).label('total')).first().total)
      else:
        total = float(Accesorio.query.filter(Accesorio.acc_clase == clase, Accesorio.acc_color == color).with_entities(func.sum(Accesorio.acc_cantidad).label('total')).first().total)
    else:
      total = float(Accesorio.query.filter(Accesorio.acc_clase == clase).with_entities(func.sum(Accesorio.acc_cantidad).label('total')).first().total)

  cant_pedida = 0
  if fecha:
    pedidos = Pedido.query.filter(Pedido.ped_fecha_evento == fecha)
    for pedido in pedidos:
      detalle = Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero, Det_pedido.det_clase == clase).first()
      if detalle:
        if color and int(color) == detalle.det_color:
            if estilo and int(estilo) == detalle.det_estilo:
              cant_pedida += float(detalle.det_pedida)
            else:
              cant_pedida += float(detalle.det_pedida)
        else:
          cant_pedida += float(detalle.det_pedida)

  cantidad = total - cant_pedida

  return jsonify(cantidad = cantidad)

@app.route('/_cargar_pedido')
def cargar_pedido():
    id = request.args.get('id')
    mod = request.args.get('mod')
    permiso = admin_permission.can()
    pedido = None
    if not id:
      if int(mod) == 1:
        pedido = Pedido.query.order_by(Pedido.ped_numero).first()
      elif int(mod) == -1:
        pedido = Pedido.query.order_by(Pedido.ped_numero.desc()).first()
    else:
      if int(mod) == 1:
        pedido = Pedido.query.filter(Pedido.ped_numero > id).order_by(Pedido.ped_numero).first()
      elif int(mod) == -1:
        pedido = Pedido.query.filter(Pedido.ped_numero < id).order_by(Pedido.ped_numero.desc()).first()
      else:
        pedido = Pedido.query.get(id)

    if not pedido:
      return jsonify(id = id)

    detalles = []
    det_estola = None
    for detalle in Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero):
      detalles.append(detalle.serialize)
      if detalle.det_clase == 4:
        det_estola = Det_estola.query.filter(Det_estola.etl_detalle == detalle.det_id).first()
        if det_estola:
          det_estola = det_estola.serialize

    institucion = Institucion.query.get(pedido.ped_institucion)

    return jsonify(id = pedido.ped_numero, cliente = float(pedido.ped_cliente), institucion = institucion.serialize, pedido = pedido.serialize, detalles = detalles, estola = det_estola, permiso = permiso)
    
@app.route('/_cargar_orden')
def cargar_orden():
  id_pedido = request.args.get('id_pedido')
  id_motivo = request.args.get('id_motivo')
  despacho = Despacho.query.filter(Despacho.des_pedido == id_pedido, Despacho.des_prestamo == id_motivo).first()
  if despacho:
    detalles = []
    for det_despacho in Det_despacho.query.filter(Det_despacho.tal_despacho == despacho.des_id).all():
      detalle = det_despacho.serialize
      detalle['talla'] = Talla.query.get(det_despacho.tal_talla).tal_nombre
      detalles.append(detalle)
    orden = Orden.query.filter(Orden.ord_despacho == despacho.des_id, Orden.ord_tipo == 1).first()
    entrega = orden.serialize
    if orden.ord_hora:
      entrega['hora'] = orden.ord_hora.strftime('%I:%M %p')
    else:
      entrega['hora'] = None
    if orden.ord_personalizada:
      personalizada = Personalizada.query.get(orden.ord_personalizada)
      entrega.update({'personalizada': personalizada.serialize})
    else:
      transportadora = Transportadora.query.get(orden.ord_transportadora)
      entrega.update({'transportadora': transportadora.serialize})
    
    orden = Orden.query.filter(Orden.ord_despacho == despacho.des_id, Orden.ord_tipo == 2).first()
    recogida = orden.serialize
    if orden.ord_personalizada:
      personalizada = Personalizada.query.get(orden.ord_personalizada)
      recogida.update({'personalizada': personalizada.serialize})
    else:
      transportadora = Transportadora.query.get(orden.ord_transportadora)
      recogida.update({'transportadora': transportadora.serialize})

    return jsonify(flag = True, despacho = despacho.serialize, entrega = entrega, recogida = recogida, detalles = detalles)
  else:
    return jsonify(flag = False)

@app.route('/_permiso_requerido')
@admin_permission.require()
def permiso_requerido():
  return jsonify(data = True)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + 'pdf/', filename, as_attachment=True)

@app.route('/_descargar_pdf')
def descargar_pdf():
  id_fac = request.args.get('id_fac')
  id_cli = request.args.get('id_cli')
  resumen = gen_resumen(id_fac,id_cli)
  file = 'pedido.pdf'
  gen_pdf(id, resumen, file)
  return jsonify(result = True)

@app.route('/_descargar_pdf_despacho')
def descargar_pdf_despacho():
  id = request.args.get('id')
  id_motivo = request.args.get('id_motivo')
  try:
    resumen = gen_resumen(id)
    file = 'orden_despacho.pdf'
    gen_pdf_des(id, resumen, file, id_motivo = id_motivo)
    return jsonify(result = True)
  except Exception:
    return jsonify(result = False)

@app.route('/_descargar_pdf_entrega_recogida')
def descargar_pdf_entrega_recogida():
  id = request.args.get('id')
  id_motivo = request.args.get('id_motivo')
  try:
    pedido = Pedido.query.get(id)
    file = 'orden_entrega_recogida.pdf'
    gen_pdf_ent_rec(id, file, id_motivo = id_motivo)
    return jsonify(result = True)
  except Exception:
    return jsonify(result = False)

@app.route('/_descargar_pdf_ordenes')
def descargar_pdf_ordenes():
  fecha = request.args.get('fecha')
  try:
    fecha = datetime.strptime(fecha, '%Y-%m-%d')
    despachos = Despacho.query.filter(Despacho.des_fecha_entrega == fecha)
    files = []
    for despacho in despachos:
      id_motivo = despacho.des_prestamo
      id_pedido = despacho.des_pedido
      resumen = gen_resumen(id_pedido)
      file = 'orden_despacho_' + str(despacho.des_id) + '.pdf'
      files.append(file)
      gen_pdf_des(id_pedido, resumen, file, id_motivo = id_motivo)

    zip_name = 'ordenes_despacho.zip'
    with ZipFile(os.path.join(app.config['UPLOAD_FOLDER'], 'pdf/' + zip_name), 'w') as myzip:
      for file in files:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pdf/' + file) 
        myzip.write(filename, os.path.basename(filename))
        os.remove(filename)
    return jsonify(flag = True)
  except Exception:
    return jsonify(flag = False)

@app.route('/_descargar_pdf_ordenes_ent_rec')
def descargar_pdf_ordenes_ent_rec():
  fecha = request.args.get('fecha')
  try:
    fecha = datetime.strptime(fecha, '%Y-%m-%d')
    entregas = Orden.query.filter(Orden.ord_tipo == 1, Orden.ord_fecha == fecha)
    files = []
    for entrega in entregas:
      despacho = Despacho.query.get(entrega.ord_despacho)
      id_motivo = despacho.des_prestamo
      id_pedido = despacho.des_pedido
      resumen = gen_resumen(id_pedido)
      file = 'orden_entrega_recogida_' + str(despacho.des_id) + '.pdf'
      files.append(file)
      gen_pdf_ent_rec(id_pedido, file, id_motivo = id_motivo)

    zip_name = 'ordenes_entrega_recogida.zip'
    with ZipFile(os.path.join(app.config['UPLOAD_FOLDER'], 'pdf/' + zip_name), 'w') as myzip:
      for file in files:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pdf/' + file) 
        myzip.write(filename, os.path.basename(filename))
        os.remove(filename)
    return jsonify(flag = True)
  except Exception:
    return jsonify(flag = False)

@app.route('/_cargar_horas_entrega_des')
def cargar_horas_entrega_des():
  fecha = request.args.get('fecha')
  hora = request.args.get('hora')
  despachos = Despacho.query.filter(Despacho.des_fecha_entrega == fecha).all()
  horas = []
  for d in despachos:
    if d.des_hora_entrega:
      horas.append(d.des_hora_entrega.strftime('%I:%M %p'))
  if hora and hora in horas:
    horas.remove(hora)
  horas = timeRange(horas_usadas = horas)
  return jsonify(horas = horas)

@app.route('/_cargar_horas_entrega')
def cargar_horas_entrega():
  fecha = request.args.get('fecha')
  hora = request.args.get('hora')
  ordenes = Orden.query.filter(Orden.ord_tipo == 1, Orden.ord_fecha == fecha).all()
  horas = []
  for o in ordenes:
    if o.ord_hora:
      horas.append(o.ord_hora.strftime('%I:%M %p'))
  if hora and hora in horas:
    horas.remove(hora)
  horas = timeRange(horas_usadas = horas)
  return jsonify(horas = horas)

@app.route('/_obtener_fechas')
def obtener_fechas():
  fecha_evento = request.args.get('fecha_evento')
  if fecha_evento:
    fecha_evento = datetime.strptime(fecha_evento, '%Y-%m-%d')
    delta = timedelta(days=1)

    id = request.args.get('ciudad')
    ciudad = Ciudad.query.get(id)
    if ciudad and ciudad.ciu_metropol == 0:
      dias = 2
    else:
      dias = 1
    fecha_entrega = fecha_evento
    fecha_recogida = fecha_evento

    while dias > 0:
      fecha_entrega -= delta
      if int(fecha_entrega.strftime('%w')) == 0:
        fecha_entrega -= delta
      
      fecha_recogida += delta
      if int(fecha_recogida.strftime('%w')) == 0:
        fecha_recogida += delta
      dias -= 1
  
    return jsonify(fecha_entrega = fecha_entrega.strftime('%Y-%m-%d'), fecha_recogida = fecha_recogida.strftime('%Y-%m-%d'), flag = True)
  else:
    return jsonify(flag = False)

@app.route('/_obtener_fecha_despacho')
def obtener_fecha_despacho():
  fecha_entrega = request.args.get('fecha_entrega')
  if fecha_entrega:
    fecha_entrega = datetime.strptime(fecha_entrega, '%Y-%m-%d')
    delta = timedelta(days=1)

    fecha_despacho = fecha_entrega - delta
    if int(fecha_despacho.strftime('%w')) == 0:
      fecha_despacho -= delta

    return jsonify(fecha_despacho = fecha_despacho.strftime('%Y-%m-%d'), flag = True)
  else:
    return jsonify(flag = False)

def gen_resumen(id_cli,id_fac):
  
  cliente = Factura.query.get(fac_cliente).where(fac_numero = id_fac)
  tipoPedido = Factura.query.get(fac_tipoPedido).where(fac_numero = id_fac)
  ReferenciaNombretipoPedido = Factura.query.get(fac_ReferenciaNombre).where(fac_numero = id_fac)
  ReferenciaCelular = Factura.query.get(fac_ReferenciaCelular).where(fac_numero = id_fac)
  ReferenciaMedio = Factura.query.get(fac_ReferenciaMedio).where(fac_numero = id_fac)
  poblacion = Factura.query.get(fac_poblacion).where(fac_numero = id_fac)
  evento = Factura.query.get(fac_evento).where(fac_numero = id_fac)
  eventoDia = Factura.query.get(fac_eventoDia).where(fac_numero = id_fac)
  eventoMes = Factura.query.get(fac_eventoMes).where(fac_numero = id_fac)
  eventoAño = Factura.query.get(fac_eventoAño).where(fac_numero = id_fac)
  ReferenciaProducto1 = Factura.query.get(fac_ReferenciaProducto1).where(fac_numero = id_fac)
  ReferenciaProducto2 = Factura.query.get(fac_ReferenciaProducto2).where(fac_numero = id_fac)
  ReferenciaProducto3 = Factura.query.get(fac_ReferenciaProducto3).where(fac_numero = id_fac)
  ReferenciaProducto4 = Factura.query.get(fac_ReferenciaProducto4).where(fac_numero = id_fac)
  descripcion1 = Factura.query.get(fac_descripcion1).where(fac_numero = id_fac)
  descripcion2 = Factura.query.get(fac_descripcion2).where(fac_numero = id_fac)
  descripcion3 = Factura.query.get(fac_descripcion3).where(fac_numero = id_fac)
  descripcion4 = Factura.query.get(fac_descripcion4).where(fac_numero = id_fac)
  accesorios1 = Factura.query.get(fac_accesorios1).where(fac_numero = id_fac)
  accesorios2 = Factura.query.get(facaccesorios2).where(fac_numero = id_fac)
  accesorios3 = Factura.query.get(fac_accesorios3).where(fac_numero = id_fac)
  accesorios4 = Factura.query.get(fac_accesorios4).where(fac_numero = id_fac)
  MedidasArreglos1 = Factura.query.get(fac_MedidasArreglos1).where(fac_numero = id_fac)
  MedidasArreglos2 = Factura.query.get(fac_MedidasArreglos2).where(fac_numero = id_fac)
  MedidasArreglos3 = Factura.query.get(fac_MedidasArreglos3).where(fac_numero = id_fac)
  MedidasArreglos4 = Factura.query.get(fac_MedidasArreglos4).where(fac_numero = id_fac)
  ValorReferencia1 = Factura.query.get(fac_ValorReferencia1).where(fac_numero = id_fac)
  ValorReferencia2 = Factura.query.get(fac_ValorReferencia2).where(fac_numero = id_fac)
  ValorReferencia3 = Factura.query.get(fac_ValorReferencia3).where(fac_numero = id_fac)
  ValorReferencia4 = Factura.query.get(fac_ValorReferencia4).where(fac_numero = id_fac)
  fac_Total = Factura.query.get(fac_Total).where(fac_numero = id_fac)
  fac_Abono = Factura.query.get(fac_Abono).where(fac_numero = id_fac)
  fac_Saldo = Factura.query.get(fac_Saldo).where(fac_numero = id_fac)
  ReclamarMercanciaDia = Factura.query.get(fac_ReclamarMercanciaDia).where(fac_numero = id_fac)
  ReclamarMercanciaMes = Factura.query.get(fac_ReclamarMercanciaMes).where(fac_numero = id_fac)
  ReclamarMercanciaAño = Factura.query.get(fac_ReclamarMercanciaAño).where(fac_numero = id_fac)
  DevolverMercanciaDia = Factura.query.get(fac_DevolverMercanciaDia).where(fac_numero = id_fac)
  DevolverMercanciaMes = Factura.query.get(fac_DevolverMercanciaMes).where(fac_numero = id_fac)
  DevolverMercanciaAño = Factura.query.get(fac_DevolverMercanciaAño).where(fac_numero = id_fac)
  AtendioPor = Factura.query.get(fac_AtendioPor).where(fac_numero = id_fac)
  consecutivoManual = Factura.query.get(fac_consecutivoManual).where(fac_numero = id_fac)
  nota = Factura.query.get(fac_nota).where(fac_numero = id_fac)

  cli_nombre = Cliente.query.get(cli_nombre).where(cli_identificacion = id_cli)
  cli_ciudad = Cliente.query.get(cli_ciudad).where(cli_identificacion = id_cli)
  cli_direccion = Cliente.query.get(cli_direccion).where(cli_identificacion = id_cli)
  cli_email = Cliente.query.get(cli_email).where(cli_identificacion = id_cli)
  cli_celular = Cliente.query.get(cli_celular).where(cli_identificacion = id_cli)
  cli_telefono = Cliente.query.get(cli_telefono).where(cli_identificacion = id_cli)
  cli_extension = Cliente.query.get(cli_extension).where(cli_identificacion = id_cli)
  cli_barrio = Cliente.query.get(cli_barrio).where(cli_identificacion = id_cli)
  cli_nacido_mes = Cliente.query.get(cli_nacido_mes).where(cli_identificacion = id_cli)
  cli_nacido_dia = Cliente.query.get(cli_nacido_dia).where(cli_identificacion = id_cli)
  

  

  resumen = [id_fac, tipoPedido, ReferenciaNombretipoPedido, ReferenciaCelular,ReferenciaMedio, poblacion, evento, eventoDia, eventoMes, eventoAño, ReferenciaProducto1,ReferenciaProducto2,ReferenciaProducto3,ReferenciaProducto4,descripcion1,descripcion2,descripcion3,descripcion4,accesorios1,accesorios2,accesorios3,accesorios4,MedidasArreglos1,MedidasArreglos2,MedidasArreglos3,MedidasArreglos4,ValorReferencia1,ValorReferencia2,ValorReferencia3,ValorReferencia4,fac_Total,fac_Abono,fac_Saldo,ReclamarMercanciaDia,ReclamarMercanciaMes,ReclamarMercanciaAño,DevolverMercanciaDia,DevolverMercanciaMes,DevolverMercanciaAño,AtendioPor,consecutivoManual,nota,cli_nombre,cli_ciudad,cli_direccion,cli_email,cli_celular,cli_telefono,cli_extension,cli_barrio,cli_nacido_mes,cli_nacido_dia]

  return resumen


##### Generador de PDF's
def create_pdf(pdf_data, filename):
    pdf = open(os.path.join(app.config['UPLOAD_FOLDER'], 'pdf/' + filename), 'wb')
    pisa.CreatePDF(BytesIO(pdf_data.encode('utf-8')), pdf)
    pdf.close() 

    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(pdf_data.encode('utf-8')), pdf)
    return pdf

def gen_pdf(id, resumen, file):
  pedido = Pedido.query.get(id)
  vendedor = Usuario.query.get(pedido.ped_vendedor)
  temporada = get_temporada(pedido.ped_fecha_evento) 
  if pedido.ped_poblacion == 1:
    poblacion = 'Adultos'
  else:
    poblacion = 'Niños'
  det_pedido = {'evento': Evento.query.get(pedido.ped_evento).eve_nombre, 'jornada': Jornada.query.get(pedido.ped_jornada).jor_nombre, 'nivel': Nivele.query.get(pedido.ped_nivel).niv_nombre, 'poblacion': poblacion, 'fecha': pedido.ped_fecha.strftime('%b-%d-%Y %H:%M %p'), 'vendedor': vendedor.usu_nombre + ' ' + vendedor.usu_apellido, 'fecha_evento':  date_format(pedido.ped_fecha_evento), 'estado_com': Estado_com.query.get(pedido.ped_estado_com).esc_nombre, 'temporada': temporada}

  empresa = Empresa.query.get(pedido.ped_empresa)


  cliente = Cliente.query.get(pedido.ped_cliente)
  meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  if cliente.cli_nacido_mes:
    mes = meses[cliente.cli_nacido_mes - 1]
  else:
    mes = None
  det_cliente = {'ciudad': Ciudad.query.get(cliente.cli_ciudad).ciu_nombre , 'cargo': Cargo.query.get(cliente.cli_cargo).crg_descripcion, 'mes': mes}


  institucion = Institucion.query.get(pedido.ped_institucion)
  ciudad = Ciudad.query.get(institucion.ins_ciudad)
  det_institucion = {'ciudad': ciudad.ciu_nombre, 'metro': ciudad.ciu_metropol}

  detalles = Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero)

  det_estola = None
  tipo_estola = None
  tipo = None
  clases = []
  colores = []
  estilos = []
  cortesias = 0
  for detalle in detalles:
    cortesias += int(detalle.det_cortesia)
    if detalle.det_clase:
      clases.append(Clase.query.get(detalle.det_clase))
    if detalle.det_color:
      colores.append(Color.query.get(detalle.det_color))
    if detalle.det_estilo:
      estilos.append(Estilo.query.get(detalle.det_estilo))
    if detalle.det_clase == 4:
      if Det_estola.query.filter(Det_estola.etl_detalle == detalle.det_id).first():
        det_estola = Det_estola.query.filter(Det_estola.etl_detalle == detalle.det_id).first()
        if det_estola.etl_tipo:
          tipo = Tipo.query.get(det_estola.etl_tipo).tip_nombre
        if det_estola.etl_tipo_escudo:
          tipo_estola = Tipo_estola.query.get(det_estola.etl_tipo_escudo).tes_nombre

  for i,valor in enumerate(resumen):
    if valor and valor != 'None':
      resumen[i] = format(float(valor),',.2f')
  pdf = create_pdf(render_template("factura.html", pedido = pedido, cliente = cliente, institucion = institucion, detalles = detalles, det_cliente = det_cliente, det_institucion = det_institucion, det_pedido = det_pedido, cortesias = cortesias, estola = det_estola, tipo = tipo, tipo_estola = tipo_estola, colores = colores, estilos = estilos, clases = clases, resumen = resumen, empresa = empresa, path = os.path.abspath(os.path.dirname(__file__))), file)

  return pdf

def send_pdf(id, resumen, enviar):
  file = 'pedido.pdf'
  pdf = gen_pdf(id, resumen, file)
  if enviar:
    pedido = Pedido.query.get(id)
    cliente = Cliente.query.get(pedido.ped_cliente)
    institucion = Institucion.query.get(pedido.ped_institucion)
    vendedor = Usuario.query.get(pedido.ped_vendedor)
    det_pedido = {'evento': Evento.query.get(pedido.ped_evento).eve_nombre, 'jornada': Jornada.query.get(pedido.ped_jornada).jor_nombre, 'nivel': Nivele.query.get(pedido.ped_nivel).niv_nombre, 'fecha': pedido.ped_fecha.strftime('%b-%d-%Y %H:%M %p'), 'vendedor': vendedor.usu_nombre + ' ' + vendedor.usu_apellido, 'fecha_evento':  date_format(pedido.ped_fecha)}


    subject = "Pedido No. " + str(pedido.ped_numero) + " " + pedido.ped_fecha_mod.strftime('%b-%d-%Y %H:%M %p')
    receiver = cliente.cli_email
    msg = Message(subject=subject, sender='losdelastogas@gmail.com', recipients=[receiver])
    msg.body = "Pedido No. " + str(pedido.ped_numero) + " \nFecha de creación: " + det_pedido['fecha'] + "\nFecha de modificación: " + pedido.ped_fecha_mod.strftime('%b-%d-%Y %H:%M %p') + "\nInstitución: " + institucion.ins_nombre + " NIT: " + str(institucion.ins_nit) + "\nEncargado: " + cliente.cli_nombre + " " + cliente.cli_apellido + " Identificación: " + str(cliente.cli_identificacion)
    msg.attach(file, "application/pdf", pdf.getvalue())
    mail_ext.send(msg)
  return file

def gen_pdf_des(id, resumen, file, id_motivo = None):
  pedido = Pedido.query.get(id)
  det_pedido = {'evento': Evento.query.get(pedido.ped_evento).eve_nombre, 'jornada': Jornada.query.get(pedido.ped_jornada).jor_nombre, 'nivel': Nivele.query.get(pedido.ped_nivel).niv_nombre, 'fecha': pedido.ped_fecha.strftime('%b-%d-%Y %H:%M %p')}
  
  vendedor = Usuario.query.get(pedido.ped_vendedor) 
  empresa = Empresa.query.get(pedido.ped_empresa)

  if id_motivo:
    despacho = Despacho.query.filter(Despacho.des_pedido == pedido.ped_numero, Despacho.des_prestamo == id_motivo).first()  
  else:
    despacho = Despacho.query.filter(Despacho.des_pedido == pedido.ped_numero).order_by(Despacho.des_fecha_mod.desc()).first()
  tallas = Det_despacho.query.filter(Det_despacho.tal_despacho == despacho.des_id)
  nom_tallas = []
  total_empacada = 0
  for talla in tallas:
    nom_tallas.append(Talla.query.get(talla.tal_talla))
    total_empacada += talla.tal_cantidad

  detalles = Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero)

  clases = []
  colores = []
  estilos = []
  for detalle in detalles:
    if detalle.det_clase:
      clases.append(Clase.query.get(detalle.det_clase))
    if detalle.det_color:
      colores.append(Color.query.get(detalle.det_color))
    if detalle.det_estilo:
      estilos.append(Estilo.query.get(detalle.det_estilo))

  det_despacho = []

  if despacho.des_prestamo:
    det_despacho.append(Prestamo.query.get(despacho.des_prestamo).prs_nombre)
  else:
    det_despacho.append('')
  if despacho.des_presindiv:
    det_despacho.append(Presindiv.query.get(despacho.des_presindiv).pri_nombre)
  else:
    det_despacho.append('')
  if despacho.des_prespedido:
    det_despacho.append(Prespedido.query.get(despacho.des_prespedido).prp_nombre)
  else:
    det_despacho.append('')
  if despacho.des_fecha:
    det_despacho.append(despacho.des_fecha.strftime('%b-%d-%Y %H:%M %p'))
  else:
    det_despacho.append('')
  det_despacho.append(despacho.des_fecha_entrega.strftime('%b-%d-%Y %H:%M %p'))

  for i,valor in enumerate(resumen):
    if valor and valor != 'None':
      resumen[i] = format(float(valor),',.2f')
  
  institucion = Institucion.query.get(pedido.ped_institucion)
  ciudad = Ciudad.query.get(institucion.ins_ciudad)
  det_institucion = {'ciudad': ciudad.ciu_nombre}

  cliente = Cliente.query.get(pedido.ped_cliente)
  pdf = create_pdf(render_template("despacho.html", pedido = pedido, detalles = detalles, despacho = despacho, tallas = tallas, det_pedido = det_pedido, det_despacho = det_despacho, nom_tallas = nom_tallas, clases = clases, colores = colores, estilos = estilos, empresa = empresa, institucion = institucion, det_institucion = det_institucion, vendedor = vendedor, total_empacada = total_empacada), file)
  
  return pdf, det_despacho

def send_pdf_des(id, resumen, copia):
  pedido = Pedido.query.get(id)
  despacho = Despacho.query.filter(Despacho.des_pedido == pedido.ped_numero).order_by(Despacho.des_fecha_mod.desc()).first()
  det_pedido = {'evento': Evento.query.get(pedido.ped_evento).eve_nombre, 'jornada': Jornada.query.get(pedido.ped_jornada).jor_nombre, 'nivel': Nivele.query.get(pedido.ped_nivel).niv_nombre, 'fecha': pedido.ped_fecha.strftime('%b-%d-%Y %H:%M %p')}
  cliente = Cliente.query.get(pedido.ped_cliente)
  institucion = Institucion.query.get(pedido.ped_institucion)

  file = 'orden_despacho.pdf'
  pdf, det_despacho = gen_pdf_des(id, resumen, file)

  subject = "Orden de empaque y despacho No. " + str(despacho.des_id) + " - Pedido No. " + str(pedido.ped_numero) + " " + pedido.ped_fecha_mod.strftime('%b-%d-%Y %H:%M %p')
  if copia:
    recipients = []
    recipients.append(cliente.cli_email)
    msg = Message(subject=subject, sender='losdelastogas@gmail.com', recipients= recipients)
    msg.body = "Pedido No. "+ str(pedido.ped_numero) + " \nFecha de creación pedido: " + det_pedido['fecha'] + "\nFecha de creación Orden: " + det_despacho[3] + "\nFecha de modificación: " + pedido.ped_fecha_mod.strftime('%b-%d-%Y %H:%M %p') + "\nInstitución: " + institucion.ins_nombre + " NIT: " + str(institucion.ins_nit) + "\nEncargado: " + cliente.cli_nombre + " " + cliente.cli_apellido + " Identificación: " + str(cliente.cli_identificacion)

    # pdf = open(os.path.join(app.config['UPLOAD_FOLDER'], 'pdf/' + file), 'r')
    msg.attach(file, "application/pdf", pdf.getvalue())
    # pdf.close()
    mail_ext.send(msg)
  return file


def gen_pdf_ent_rec(id, file, id_motivo = None):
  pedido = Pedido.query.get(id)
  det_pedido = {'evento': Evento.query.get(pedido.ped_evento).eve_nombre, 'jornada': Jornada.query.get(pedido.ped_jornada).jor_nombre, 'nivel': Nivele.query.get(pedido.ped_nivel).niv_nombre, 'fecha': pedido.ped_fecha.strftime('%b-%d-%Y %H:%M %p')}
  empresa = Empresa.query.get(pedido.ped_empresa)

  if id_motivo:
    despacho = Despacho.query.filter(Despacho.des_pedido == pedido.ped_numero, Despacho.des_prestamo == id_motivo).first()
  else:
    despacho = Despacho.query.filter(Despacho.des_pedido == pedido.ped_numero).order_by(Despacho.des_fecha_mod.desc()).first()

  detalles = Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero)
  clases = []
  colores = []
  estilos = []
  for detalle in detalles:
    if detalle.det_clase:
      clases.append(Clase.query.get(detalle.det_clase))
    if detalle.det_color:
      colores.append(Color.query.get(detalle.det_color))
    if detalle.det_estilo:
      estilos.append(Estilo.query.get(detalle.det_estilo))

  entrega = Orden.query.filter(Orden.ord_despacho == despacho.des_id, Orden.ord_tipo == 1).first()
  ent_personalizada = None
  ent_transportadora = None
  det_entrega = {'tipo': Tipo_orden.query.get(entrega.ord_tipo_orden).tip_nombre, 'fecha_entrega': entrega.ord_fecha.strftime('%b-%d-%Y'), 'motivo': Prestamo.query.get(despacho.des_prestamo).prs_nombre}
  if entrega.ord_personalizada:
    ent_personalizada = Personalizada.query.get(entrega.ord_personalizada)
    if ent_personalizada.per_municipio:
      det_entrega['per_ciudad'] = Ciudad.query.get(ent_personalizada.per_municipio).ciu_nombre
    else:
      det_entrega['per_ciudad'] = None
    det_entrega['tra_ciudad'] = None
  else:
    ent_transportadora = Transportadora.query.get(entrega.ord_transportadora)
    det_entrega['per_ciudad'] = None
    if ent_transportadora.tra_municipio:
      det_entrega['tra_ciudad'] = Ciudad.query.get(ent_transportadora.tra_municipio).ciu_nombre
    else:
      det_entrega['tra_ciudad'] = None

  recogida = Orden.query.filter(Orden.ord_despacho == despacho.des_id, Orden.ord_tipo == 2).first()
  rec_personalizada = None
  rec_transportadora = None
  det_recogida = {'tipo': Tipo_orden.query.get(recogida.ord_tipo_orden).tip_nombre, 'fecha_recogida': recogida.ord_fecha.strftime('%b-%d-%Y')}
  if recogida.ord_personalizada:
    rec_personalizada = Personalizada.query.get(recogida.ord_personalizada)
    if rec_personalizada.per_municipio:
        det_recogida['per_ciudad'] = Ciudad.query.get(rec_personalizada.per_municipio).ciu_nombre
    else:
        det_recogida['per_ciudad'] = None
    det_recogida['tra_ciudad'] = None
  else:
    rec_transportadora = Transportadora.query.get(recogida.ord_transportadora)
    det_recogida['per_ciudad'] = None
    if rec_transportadora.tra_municipio:
      det_recogida['tra_ciudad'] = Ciudad.query.get(rec_transportadora.tra_municipio).ciu_nombre
    else:
      det_recogida['tra_ciudad'] = None


  cliente = Cliente.query.get(pedido.ped_cliente)
  institucion = Institucion.query.get(pedido.ped_institucion)
  ciudad = Ciudad.query.get(institucion.ins_ciudad)
  det_institucion = {'ciudad': ciudad.ciu_nombre}
  
  pdf = create_pdf(render_template("entrega_recogida.html", pedido = pedido, detalles = detalles, det_pedido = det_pedido, clases = clases, colores = colores, estilos = estilos, empresa = empresa, institucion = institucion, det_institucion = det_institucion, entrega = entrega, det_entrega = det_entrega, ent_personalizada = ent_personalizada, ent_transportadora = ent_transportadora, recogida = recogida, det_recogida = det_recogida, rec_personalizada = rec_personalizada, rec_transportadora = rec_transportadora), file)
  
  return pdf

def send_pdf_ent_rec(id, copia):
  pedido = Pedido.query.get(id)
  despacho = Despacho.query.filter(Despacho.des_pedido == pedido.ped_numero).order_by(Despacho.des_fecha_mod.desc()).first()
  det_despacho = {'fecha': despacho.des_fecha.strftime('%b-%d-%Y %H:%M %p')}
  det_pedido = {'evento': Evento.query.get(pedido.ped_evento).eve_nombre, 'jornada': Jornada.query.get(pedido.ped_jornada).jor_nombre, 'nivel': Nivele.query.get(pedido.ped_nivel).niv_nombre, 'fecha': pedido.ped_fecha.strftime('%b-%d-%Y %H:%M %p')}
  cliente = Cliente.query.get(pedido.ped_cliente)
  institucion = Institucion.query.get(pedido.ped_institucion)

  subject = "Orden de entrega y recogida No. " + str(despacho.des_id) + " - Pedido No. " + str(pedido.ped_numero) + " " + pedido.ped_fecha_mod.strftime('%b-%d-%Y %H:%M %p')
  file = 'orden_entrega_recogida.pdf'
  pdf = gen_pdf_ent_rec(id, file)
  if copia:
    recipients = []
    recipients.append(cliente.cli_email)
    msg = Message(subject=subject, sender='losdelastogas@gmail.com', recipients= recipients)
    msg.body = "Pedido No. "+ str(pedido.ped_numero) + " \nFecha de creación pedido: " + det_pedido['fecha'] + "\nFecha de creación Orden: " + det_despacho['fecha'] + "\nFecha de modificación: " + pedido.ped_fecha_mod.strftime('%b-%d-%Y %H:%M %p') + "\nInstitución: " + institucion.ins_nombre + " NIT: " + str(institucion.ins_nit) + "\nEncargado: " + cliente.cli_nombre + " " + cliente.cli_apellido + " Identificación: " + str(cliente.cli_identificacion)
    # pdf = open(os.path.join(app.config['UPLOAD_FOLDER'], 'pdf/' + file), 'r')
    msg.attach(file, "application/pdf", pdf.getvalue())
    # pdf.close()
    mail_ext.send(msg)
  return file

def send_pdf_letra(id):
  # pedido = Pedido.query.get(id)
  # despacho = Despacho.query.filter(Despacho.des_pedido == pedido.ped_numero).order_by(Despacho.des_fecha_mod.desc()).first()
  # cliente = Cliente.query.get(pedido.ped_cliente)
  # institucion = Institucion.query.get(pedido.ped_institucion)

  # subject = "Letra de cambio - Orden de empaque No. " + str(despacho.des_id) + " - Pedido No. " + str(pedido.ped_numero) + " " + pedido.ped_fecha_mod.strftime('%b-%d-%Y %H:%M %p')
  # recipients = ['losdelastogas@gmail.com']
  # msg = Message(subject=subject, sender='losdelastogas@gmail.com', recipients= recipients)
  # msg.body = "Pedido No. "+ str(pedido.ped_numero) + " \nOrden de empaque No: " + str(despacho.des_id) + "\nInstitución: " + institucion.ins_nombre + " NIT: " + str(institucion.ins_nit) + "\nEncargado: " + cliente.cli_nombre + " " + cliente.cli_apellido + " Identificación: " + str(cliente.cli_identificacion)

  file = 'letra.pdf'
  pdf = gen_pdf_letra(id, file)
  # msg.attach(file, "application/pdf", pdf.getvalue())
  # mail_ext.send(msg)
  return file

def gen_pdf_letra(id, file):
  pedido = Pedido.query.get(id)

  detalles = Det_pedido.query.filter(Det_pedido.det_pedido == pedido.ped_numero)
  clases = []
  colores = []
  estilos = []
  for detalle in detalles:
    if detalle.det_clase:
      clases.append(Clase.query.get(detalle.det_clase))
    if detalle.det_color:
      colores.append(Color.query.get(detalle.det_color))
    if detalle.det_estilo:
      estilos.append(Estilo.query.get(detalle.det_estilo))

  recogida = Orden.query.filter(Orden.ord_tipo == 2, Orden.ord_pedido == pedido.ped_numero).order_by(Orden.ord_fecha_mod.desc()).first()
  rec_fecha = recogida.ord_fecha
  fecha = recogida.ord_fecha_mod
  entrega = Orden.query.filter(Orden.ord_tipo == 1, Orden.ord_pedido == pedido.ped_numero).order_by(Orden.ord_fecha_mod.desc()).first()
  if entrega.ord_personalizada:
    personalizada = Personalizada.query.get(entrega.ord_personalizada)
    cliente = personalizada.per_encargado
    cedula = personalizada.per_cedula
  elif entrega.ord_transportadora:
    transportadora = Transportadora.query.get(entrega.ord_transportadora)
    cliente = transportadora.tra_encargado
    cedula = transportadora.tra_cedula

  despacho = Despacho.query.filter(Despacho.des_pedido == pedido.ped_numero).order_by(Despacho.des_fecha_mod.desc()).first()
  des_detalles = Det_despacho.query.filter(Det_despacho.tal_despacho == despacho.des_id).all()
  cantidad = 0
  for detalle in des_detalles:
    cantidad += detalle.tal_cantidad

  valor = cantidad * 60000
  meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  det_letra = {'valor': valor, 'valorLetras': numero_a_letras(valor), 'rec_fecha': rec_fecha.strftime('%d') + ' de ' + meses[int(rec_fecha.strftime('%m')) - 1] + ' del año ' + rec_fecha.strftime('%Y'), 'fecha': fecha.strftime('%d') + ' de ' + meses[int(fecha.strftime('%m')) - 1] + ' del año ' + rec_fecha.strftime('%Y'), 'cantidad': cantidad}
  pdf = create_pdf(render_template("letra.html", pedido = pedido, detalles = detalles, clases = clases, colores = colores, estilos = estilos, cliente = cliente, cedula = cedula, det_letra = det_letra, path = os.path.abspath(os.path.dirname(__file__))), file)
  return pdf
  
  
  
  
  
  
  
  if form.validate_on_submit():
      # Create/Update del client
      if Cliente.query.get(form.identificacion_enc.data) is None:
        new_cli = Cliente(form.identificacion_enc.data, form.nombre_enc.data, form.municipio_enc.data, form.direccion_enc.data,form.email_enc.data,form.celular_enc.data, form.telefono_enc.data, form.extension_enc.data,form.barrio_enc.data, form.cli_medioConocio.data, form.mes_enc.data, form.dia_enc.data)
        db.session.add(new_cli)
        db.session.commit()
      else:
        Cliente.query.filter(Cliente.cli_identificacion == form.identificacion_enc.data).update({Cliente.cli_nombre: form.nombre_enc.data, Cliente.cli_ciudad: form.municipio_enc.data, Cliente.cli_direccion: form.direccion_enc.data,form.cli_Cliente.cli_medioConocio: form.cli_medioConocio.data, Cliente.cli_nacido_mes: form.mes_enc.data, Cliente.cli_nacido_dia: form.dia_enc.data, Cliente.cli_email: form.email_enc.data, Cliente.cli_celular: form.celular_enc.data, Cliente.cli_telefono: form.telefono_enc.data, Cliente.cli_extension: form.extension_enc.data, Cliente.cli_barrio: form.barrio_enc.data, Cliente.cli_modifica: current_user.usu_login, Cliente.cli_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
        db.session.commit()
      
      if Factura.query.get(form.fac_numero.data) is None:
        new_fac = Factura(form.identificacion_enc.data, form.fac_tipoPedido.data, form.ped_referenciaNombre.data, form.ped_referenciaCelular.data, form.ped_referenciaTelefono.data, form.ped_poblacion.data, form.ped_evento.data, form.fac_eventoDia.data, form.fac_eventoMes.data, form.fac_eventoAño.data , form.fac_ReferenciaProducto1.data, form.fac_ReferenciaProducto2.data, form.fac_ReferenciaProducto3.data, form.fac_ReferenciaProducto4.data, form.fac_descripcion1.data, form.fac_descripcion2.data, form.fac_descripcion3.data, form.fac_descripcion4.data, form.fac_accesorios1.data, form.fac_accesorios2.data, form.fac_accesorios3.data, form.fac_accesorios4.data, form.fac_MedidasArreglos1.data, form.fac_MedidasArreglos2.data, form.fac_MedidasArreglos3.data, form.fac_MedidasArreglos4.data, form.fac_ValorReferencia1.data, form.fac_ValorReferencia2.data, form.fac_ValorReferencia3.data, form.fac_ValorReferencia4.data, form.fac_Total.data, form.fac_Abono.data, form.fac_Saldo.data, form.fac_ReclamarMercanciaDia.data, form.fac_ReclamarMercanciaMes.data, form.fac_ReclamarMercanciaDia.data, form.fac_DevolverMercanciaDia.data, form.fac_DevolverMercanciaMes.data, form.fac_DevolverMercanciaAño.data, current_user.usu_login, form.ped_manual.data)
        db.session.add(new_fac)
        db.session.commit()
      else:
        Factura.query.filter(Factura.fac_numero == form.fac_numero.data).update({Factura.fac_cliente: form.fac_cliente.data, Factura.fac_tipoPedido: form.fac_tipoPedido.data, Factura.fac_ReferenciaNombre: form.fac_ReferenciaNombre.data,Factura.fac_ReferenciaCelular: form.fac_ReferenciaCelular.data,  Factura.fac_poblacion: form.fac_poblacion.data, Factura.fac_evento: form.fac_evento.data, Factura.fac_eventoDia: form.fac_eventoDia.data,Factura.fac_eventoMes: form.fac_eventoMes.data,Factura.fac_eventoAño: form.fac_eventoAño.data, Factura.fac_ReferenciaProducto1: form.fac_ReferenciaProducto1.data,Factura.fac_ReferenciaProducto2: form.fac_ReferenciaProducto2.data,Factura.fac_ReferenciaProducto3: form.fac_ReferenciaProducto3.data,Factura.fac_ReferenciaProducto4: form.fac_ReferenciaProducto4.data, Factura.fac_descripcion1: form.fac_descripcion1.data,Factura.fac_descripcion2: form.fac_descripcion2.data,Factura.fac_descripcion3: form.fac_descripcion3.data,Factura.fac_descripcion4: form.fac_descripcion4.data,Factura.fac_accesorios1: form.fac_accesorios1.data, Factura.fac_accesorios2: form.fac_accesorios2.data, Factura.fac_accesorios3: form.fac_accesorios3.data, Factura.fac_accesorios4: form.fac_accesorios4.data, Factura.fac_MedidasArreglos1: form.fac_MedidasArreglos1.data,Factura.fac_MedidasArreglos2: form.fac_MedidasArreglos2.data,Factura.fac_MedidasArreglos3: form.fac_MedidasArreglos3.data,Factura.fac_MedidasArreglos4: form.fac_MedidasArreglos4.data, Factura.fac_ValorReferencia1: form.fac_ValorReferencia1.data,Factura.fac_ValorReferencia2: form.fac_ValorReferencia2.data,Factura.fac_ValorReferencia3: form.fac_ValorReferencia3.data,Factura.fac_ValorReferencia4: form.fac_ValorReferencia4.data, Factura.fac_Total: form.fac_Total.data, Factura.fac_Abono: form.fac_Abono.data,Factura.fac_Saldo : form.fac_Saldo.data, Factura.fac_ReclamarMercanciaDia : form.fac_ReclamarMercanciaDia.data, Factura.fac_ReclamarMercanciaMes : form.fac_ReclamarMercanciaMes.data, Factura.fac_ReclamarMercanciaAño : form.fac_ReclamarMercanciaAño.data, Factura.fac_DevolverMercanciaDia : form.fac_DevolverMercanciaDia.data, Factura.fac_DevolverMercanciaMes : form.fac_DevolverMercanciaMes.data, Factura.fac_DevolverMercanciaAño : form.fac_DevolverMercanciaAño.data, Factura.fac_AtendidoPor: current_user.usu_login, Factura.fac_consecutivoManual : form.fac_consecutivoManual.data, Factura.nota : form.fac_nota.data , Factura.fac_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
        db.session.commit()




