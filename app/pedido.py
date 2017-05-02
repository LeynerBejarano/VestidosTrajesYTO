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
from app.utils import numero_a_letras, timeRange, get_temporada, text_to_time


@app.route('/pedidos', methods=['GET', 'POST'])
@login_required
def pedidos():
    datos = {'title' : 'Facturación Casa Luifer'}

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


    #### Creacion de arreglos usados en el auto-completar de jquery
    cedulas = []
    ins_data = []
    for cli in Cliente.query:
      cedulas.append(int(cli.cli_identificacion))

    form = Form_Pedido()

    #### Agregar entradas a los FieldList solo cuando se carga la pagina, para evitar datos duplicados en la validacion

    if not form.is_submitted():
        for clase in clases:
          form.detalles.append_entry()
        for talla in tallas:
          form.tallas.append_entry()

    ### Volcado de datos en el fieldlist Detalles

    for i,clase in enumerate(clases):
      form.detalles[i].clase.label = clase.cla_nombre
      form.detalles[i].clase.data = clase.cla_id

      ### Agregar a los selectores de los detalles solo los colores/estilos de las prendas/accesorios que existen en la base de datos

      ###Colores
      prendas = Prenda.query.filter(Prenda.pre_clase == clase.cla_id).group_by(Prenda.pre_color)
      accesorios = Accesorio.query.filter(Accesorio.acc_clase == clase.cla_id).group_by(Accesorio.acc_color)

      if prendas.all():
        choices = [(prenda.pre_color, Color.query.get(prenda.pre_color).col_nombre) for prenda in prendas]
      elif accesorios.all():
        choices = [(accesorio.acc_color, Color.query.get(accesorio.acc_color).col_nombre) for accesorio in accesorios]
      else:
        choices = []
      choices.sort(key=lambda tup: tup[1])
      form.detalles[i].color.choices = choices

      #Color de los sesgos igual al de las estolas
      if clase.cla_id == 4:
        form.sesgo_color.choices = choices

      ###Estilos
      prendas = Prenda.query.filter(Prenda.pre_clase == clase.cla_id).group_by(Prenda.pre_estilo).order_by(Prenda.pre_estilo)
      accesorios = Accesorio.query.filter(Accesorio.acc_clase == clase.cla_id).group_by(Accesorio.acc_estilo).order_by(Accesorio.acc_estilo)

      if prendas.all():
        choices = [(prenda.pre_estilo, Estilo.query.get(prenda.pre_estilo).est_nombre) for prenda in prendas]
      elif accesorios.all():
        choices = [(accesorio.acc_estilo, Estilo.query.get(accesorio.acc_estilo).est_nombre) for accesorio in accesorios]
      else:
        choices = []
      choices.sort()
      form.detalles[i].estilo.choices = choices

      if clase.cla_id == 4:
        form.acabado.choices = choices



    ### Volcado de datos en otros selectores/Radio buttons del formulario

    choices = [(p.pri_id, p.pri_nombre) for p in presindivs] + [(-1, 'Otro')]
    form.presindiv.choices = choices
    choices = [(p.prp_id, p.prp_nombre) for p in prespedidos] + [(-1, 'Otro')]
    form.prespedido.choices = choices
    choices = [(p.prs_id, p.prs_nombre) for p in prestamos] + [(-1, 'Otro')]
    form.prestamo.choices = choices
    choices = [(t.tip_id, t.tip_nombre) for t in tipos]
    form.tipo_estola.choices = choices
    choices = [(c.ciu_id, c.ciu_nombre) for c in ciudades] + [(-1, 'Otro')]
    form.municipio_enc.choices = choices
    form.ins_ciudad.choices = choices
    form.ent_per_municipio.choices = choices
    form.ent_tra_municipio.choices = choices
    form.rec_per_municipio.choices = choices
    form.rec_tra_municipio.choices = choices
    choices = [(c.crg_id, c.crg_descripcion) for c in cargos] + [(-1, 'Otro')]
    form.cargo_enc.choices = choices
    choices = [(e.eve_id, e.eve_nombre) for e in eventos] + [(-1, 'Otro')]
    form.ped_evento.choices = choices
    choices = [(n.niv_id, n.niv_nombre) for n in niveles] + [(-1, 'Otro')]
    form.ped_nivele.choices = choices
    choices = [(j.jor_id, j.jor_nombre) for j in jornadas] + [(-1, 'Otro')]
    form.ped_jornada.choices = choices
    choices = [(e.esc_id, e.esc_nombre) for e in estados_com]
    form.ped_estado_com.choices = choices
    choices = [(e.esf_id, e.esf_nombre) for e in estados_fin]
    form.ped_estado_fin.choices = choices
    choices = [(e.esp_id, e.esp_nombre) for e in estados]
    form.ped_estado.choices = choices
    choices = [(v.usu_login, v.usu_nombre + ' ' + v.usu_apellido if v.usu_estado == 1 else 'Inactivo - ' + v.usu_nombre + ' ' + v.usu_apellido) for v in vendedores]
    form.vendedor.choices = choices
    choices = [(t.tes_id, t.tes_nombre) for t in tipos_est]
    form.tipo_imagen.choices = choices
    choices = [(p.prs_id, p.prs_nombre) for p in presentaciones]
    form.presentacion.choices = choices
    choices = [(t.ter_id, t.ter_nombre) for t in terminaciones]
    form.terminacion.choices = choices

    choices = [(t.tip_id, t.tip_nombre) for t in tipos_orden]
    form.ent_tipo_orden.choices = choices
    form.rec_tipo_orden.choices = choices
    form.tipo_entrega_ord.choices = choices
    form.tipo_recogida_ord.choices = choices

    choices = [(c.cla_id - 1, c.cla_id - 1) for c in clases]
    form.principal.choices = choices
    if not form.is_submitted():
      form.principal.data = 0

  
    form.dia_enc.choices = [(i, str(i)) for i in range(1,32)]
    ####### SUBMIT ######
    print(form.principal.data)
    if form.validate_on_submit():
      ### Creacion de parametros, al escoger la opcion 'otro'
        if form.cargo_enc.data == -1:
          new_crg = Cargo(form.otro_cargo_enc.data)
          db.session.add(new_crg)
          db.session.commit()
          form.cargo_enc.data = Cargo.query.order_by(Cargo.crg_id.desc()).first().crg_id

        if form.municipio_enc.data == -1:
          new_ciu = Ciudad(form.otro_municipio_enc.data, 0, 1, 0, current_user.usu_login, None)
          db.session.add(new_ciu)
          db.session.commit()
          form.municipio_enc.data = Ciudad.query.order_by(Ciudad.ciu_id.desc()).first().ciu_id
          notificar_ciudad(new_ciu.ciu_nombre)

        if form.ins_ciudad.data == -1:
          new_ciu = Ciudad(form.otro_ins_ciudad.data, 0, 1, 0, current_user.usu_login, None)
          db.session.add(new_ciu)
          db.session.commit()
          form.ins_ciudad.data = Ciudad.query.order_by(Ciudad.ciu_id.desc()).first().ciu_id
          notificar_ciudad(new_ciu.ciu_nombre)

        if form.ent_per_municipio.data == -1:
          new_ciu = Ciudad(form.otro_ent_per_municipio.data, 0, 1, 0, current_user.usu_login, None)
          db.session.add(new_ciu)
          db.session.commit()
          form.ins_ciudad.data = Ciudad.query.order_by(Ciudad.ciu_id.desc()).first().ciu_id
          notificar_ciudad(new_ciu.ciu_nombre)

        if form.ent_tra_municipio.data == -1:
          new_ciu = Ciudad(form.ent_tra_municipio.data, 0, 1, 0, current_user.usu_login, None)
          db.session.add(new_ciu)
          db.session.commit()
          form.ins_ciudad.data = Ciudad.query.order_by(Ciudad.ciu_id.desc()).first().ciu_id
          notificar_ciudad(new_ciu.ciu_nombre)

        if form.rec_per_municipio.data == -1:
          new_ciu = Ciudad(form.rec_per_municipio.data, 0, 1, 0, current_user.usu_login, None)
          db.session.add(new_ciu)
          db.session.commit()
          form.ins_ciudad.data = Ciudad.query.order_by(Ciudad.ciu_id.desc()).first().ciu_id
          notificar_ciudad(new_ciu.ciu_nombre)

        if form.rec_tra_municipio.data == -1:
          new_ciu = Ciudad(form.rec_tra_municipio.data, 0, 1, 0, current_user.usu_login, None)
          db.session.add(new_ciu)
          db.session.commit()
          form.ins_ciudad.data = Ciudad.query.order_by(Ciudad.ciu_id.desc()).first().ciu_id
          notificar_ciudad(new_ciu.ciu_nombre)

        if form.cargo_enc.data == -1:
          new_crg = Cargo(form.otro_cargo_enc.data)
          db.session.add(new_crg)
          db.session.commit()
          form.cargo_enc.data = Cargo.query.order_by(Cargo.crg_id.desc()).first().crg_id

        if form.ped_evento.data == -1:
          new_eve = Evento(form.otro_ped_evento.data)
          db.session.add(new_eve)
          db.session.commit()
          form.ped_evento.data = Evento.query.order_by(Evento.eve_id.desc()).first().eve_id

        if form.ped_nivele.data == -1:
          new_niv = Nivele(form.otro_ped_nivele.data)
          db.session.add(new_niv)
          db.session.commit()
          form.ped_nivele.data = Nivele.query.order_by(Nivele.niv_id.desc()).first().niv_id

        if form.ped_jornada.data == -1:
          new_jor = Jornada(form.otro_ped_jornada.data)
          db.session.add(new_jor)
          db.session.commit()
          form.ped_jornada.data = Jornada.query.order_by(Jornada.jor_id.desc()).first().jor_id

        if form.presindiv.data == -1:
          new_pri = Presindiv(form.otro_presindiv.data)
          db.session.add(new_pri)
          db.session.commit()
          form.presindiv.data = Presindiv.query.order_by(Presindiv.pri_id.desc()).first().pri_id

        if form.prespedido.data == -1:
          new_prp = Prespedido(form.otro_prespedido.data)
          db.session.add(new_prp)
          db.session.commit()
          form.prespedido.data = Prespedido.query.order_by(Prespedido.prp_id.desc()).first().prp_id

        if form.prestamo.data == -1:
          new_pre = Prestamo(form.otro_prestamo.data)
          db.session.add(new_pre)
          db.session.commit()
          form.prestamo.data = Prestamo.query.order_by(Prestamo.prs_id.desc()).first().prs_id

      # Create/Update del client
        if Cliente.query.get(form.identificacion_enc.data) is None:
          new_cli = Cliente(form.identificacion_enc.data, form.nombre_enc.data, form.apellido_enc.data, form.municipio_enc.data, form.direccion_enc.data, form.mes_enc.data, form.dia_enc.data,form.email_enc.data, form.celular_enc.data, form.telefono_enc.data, form.extension_enc.data, form.cargo_enc.data, form.barrio_enc.data, current_user.usu_login, None)
          db.session.add(new_cli)
          db.session.commit()
        else:
          Cliente.query.filter(Cliente.cli_identificacion == form.identificacion_enc.data).update({Cliente.cli_nombre: form.nombre_enc.data, Cliente.cli_apellido: form.apellido_enc.data, Cliente.cli_ciudad: form.municipio_enc.data, Cliente.cli_direccion: form.direccion_enc.data, Cliente.cli_nacido_mes: form.mes_enc.data, Cliente.cli_nacido_dia: form.dia_enc.data, Cliente.cli_email: form.email_enc.data, Cliente.cli_celular: form.celular_enc.data, Cliente.cli_telefono: form.telefono_enc.data, Cliente.cli_extension: form.extension_enc.data, Cliente.cli_cargo: form.cargo_enc.data, Cliente.cli_barrio: form.barrio_enc.data, Cliente.cli_modifica: current_user.usu_login, Cliente.cli_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
          db.session.commit()

      # Create prospecto
        if form.ped_estado_com.data == 2:
          if form.hora_entrega.data and form.hora_entrega.data != 'None':
            hora_entrega = text_to_time(form.hora_entrega.data)
          else:
            hora_entrega = None

          # Create de la institucion
          new_ins = Institucion(form.ins_nit.data, form.ins_nombre.data, form.ins_ciudad.data, current_user.usu_login, None)
          db.session.add(new_ins)
          db.session.commit()
          ins = Institucion.query.order_by(Institucion.ins_fecha_mod.desc()).first
          new_pro = Prospecto(98533266, form.identificacion_enc.data, ins.ins_id, None, form.ped_evento.data, form.ped_poblacion.data, None, form.ped_jornada.data, form.ped_nivele.data, form.vendedor.data, form.fecha_evento.data, form.hora_evento.data, form.fecha_entrega.data, hora_entrega, form.fecha_recogida.data, form.hora_recogida.data, form.tipo_entrega_ord.data, form.tipo_recogida_ord.data, form.valor_uni.data, form.abonos.data, form.ped_estado_com.data, form.ped_estado_fin.data, form.ped_estado.data, form.ped_observacion.data, form.fecha_contacto.data, form.principal.data + 1, current_user.usu_login, None)
          db.session.add(new_pro)
          db.session.commit()
          pro = Prospecto.query.order_by(Prospecto.pro_fecha_mod.desc()).first()
          numero = pro.pro_numero
          #Agregar Detalles del prospecto
          for entry in form.detalles.entries:
            if entry.data['pedida']:
              new_det = Det_prospecto(numero, entry.data['clase'], entry.data['color'], entry.data['estilo'], entry.data['detalle'], entry.data['pedida'], entry.data['cortesia'], entry.data['despachada'], entry.data['devuelta'], entry.data['entregada'], entry.data['faltante'], entry.data['recogida'], current_user.usu_login, None)
              db.session.add(new_det)
              db.session.commit()
              #Si la entrada es una estola (clase 4)
              if entry.data['clase'] == 4:
                detalle = Det_prospecto.query.filter(Det_prospecto.det_clase == 4).order_by(Det_prospecto.det_fecha_mod.desc()).first()
                if form.imagen.data.filename:
                  filename = secure_filename(form.ins_nombre.data + '.jpg')
                  form.imagen.data.save(os.path.join(app.config['UPLOAD_FOLDER'], 'estolas/' +filename))
                else:
                  filename = None
                new_est = Pro_estola(filename, detalle.det_id, form.tipo_estola.data, form.tipo_imagen.data, form.tamano_estola.data, form.doble_faz.data, form.flequillo.data, form.personalizada.data, form.terminacion.data, form.presentacion.data, form.lado_izq.data, form.lado_der.data, form.sesgo.data, form.sesgo_color.data)
                db.session.add(new_est)
                db.session.commit()
          flash(u'¡Prospecto exitosamente creado!', 'success')  
          return redirect('pedidos') 
        else:
          if form.hora_entrega.data and form.hora_entrega.data != 'None':
            hora_entrega = text_to_time(form.hora_entrega.data)
          else:
            hora_entrega = None
          label = {}
          if form.id_pedido.data and Pedido.query.get(form.id_pedido.data):
            #Update Pedido
            label['accion'] = 'actualizado'
            #Notificar cambio en el valor unitario, si este es menor al valor anterior
            old_val = Pedido.query.get(form.id_pedido.data).ped_val_unitario
            if form.valor_uni.data < old_val:
              usuario = current_user.usu_nombre + " " + current_user.usu_apellido
              notificar_valor_menor(antiguo=old_val, nuevo=form.valor_uni.data, usuario= usuario, pedido= form.id_pedido.data)

            Pedido.query.filter(Pedido.ped_numero == form.id_pedido.data).update({Pedido.ped_empresa: 98533266 , Pedido.ped_cliente: form.identificacion_enc.data, Pedido.ped_total: None , Pedido.ped_evento: form.ped_evento.data , Pedido.ped_poblacion: form.ped_poblacion.data, Pedido.ped_estilo: None , Pedido.ped_jornada: form.ped_jornada.data , Pedido.ped_nivel: form.ped_nivele.data , Pedido.ped_vendedor: form.vendedor.data , Pedido.ped_fecha_evento: form.fecha_evento.data , Pedido.ped_hora_evento: form.hora_evento.data , Pedido.ped_fecha_entrega: form.fecha_entrega.data , Pedido.ped_hora_entrega: hora_entrega, Pedido.ped_fecha_recogida: form.fecha_recogida.data , Pedido.ped_hora_recogida: form.hora_recogida.data , Pedido.ped_tipo_entrega_ord: form.tipo_entrega_ord.data, Pedido.ped_tipo_recogida_ord: form.tipo_recogida_ord.data, Pedido.ped_val_unitario: form.valor_uni.data , Pedido.ped_abono: form.abonos.data , Pedido.ped_estado_com: form.ped_estado_com.data, Pedido.ped_estado_fin: form.ped_estado_fin.data, Pedido.ped_estado: form.ped_estado.data, Pedido.ped_observacion: form.ped_observacion.data,Pedido.ped_manual: form.ped_manual.data, Pedido.ped_principal: form.principal.data + 1, Pedido.ped_modifica: current_user.usu_login, Pedido.ped_fecha_mod: datetime.now(timezone('America/Bogota'))},synchronize_session=False)
            db.session.commit()     
            ped = Pedido.query.order_by(Pedido.ped_fecha_mod.desc()).first() 

            # Update de la institucion
            Institucion.query.filter(Institucion.ins_id == ped.ped_institucion).update({ Institucion.ins_nombre: form.ins_nombre.data, Institucion.ins_nit: form.ins_nit.data, Institucion.ins_ciudad: form.ins_ciudad.data, Institucion.ins_modifica: current_user.usu_login, Institucion.ins_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
            db.session.commit()   
          else:
            # Create de la institucion
            new_ins = Institucion(form.ins_nit.data, form.ins_nombre.data, form.ins_ciudad.data, current_user.usu_login, None)
            db.session.add(new_ins)
            db.session.commit()

            #Create Pedido
            label['accion'] = 'ingresado'
            new_ped = Pedido(98533266, form.identificacion_enc.data, new_ins.ins_id, None, form.ped_evento.data, form.ped_poblacion.data, None, form.ped_jornada.data, form.ped_nivele.data, form.vendedor.data, form.fecha_evento.data, form.hora_evento.data, form.fecha_entrega.data, hora_entrega, form.fecha_recogida.data, form.hora_recogida.data, form.tipo_entrega_ord.data, form.tipo_recogida_ord.data, form.valor_uni.data, form.abonos.data, form.ped_estado_com.data, form.ped_estado_fin.data, form.ped_estado.data, form.ped_observacion.data, form.ped_manual.data, form.principal.data + 1, current_user.usu_login, None)
            db.session.add(new_ped)
            db.session.commit()
            ped = Pedido.query.order_by(Pedido.ped_fecha_mod.desc()).first()

          numero = ped.ped_numero

          ##Notificar en caso de que el valor unitario sea menor al 70% del valor sugerido
          if float(form.valor_uni.data) < (float(form.valor_sugerido.data) * 0.7):
            usuario = current_user.usu_nombre + " " + current_user.usu_apellido
            notificar_valor_sugerido(sugerido = form.valor_sugerido.data, valor = form.valor_uni.data, usuario = usuario, pedido = numero)

          #Agregar Detalles del pedido
          for entry in form.detalles.entries:
            detalle = Det_pedido.query.filter(Det_pedido.det_pedido == numero, Det_pedido.det_clase == entry.data['clase']).first()

            if detalle:
              #Update Detalle
              if entry.data['pedida']:

                Det_pedido.query.filter(Det_pedido.det_pedido == numero, Det_pedido.det_clase == entry.data['clase']).update({Det_pedido.det_pedido: numero, Det_pedido.det_clase: entry.data['clase'], Det_pedido.det_color: entry.data['color'], Det_pedido.det_estilo: entry.data['estilo'], Det_pedido.det_detalle: entry.data['detalle'], Det_pedido.det_pedida: entry.data['pedida'], Det_pedido.det_cortesia: entry.data['cortesia'], Det_pedido.det_despachada: entry.data['despachada'], Det_pedido.det_devuelta: entry.data['devuelta'], Det_pedido.det_entregada: entry.data['entregada'], Det_pedido.det_faltante: entry.data['faltante'], Det_pedido.det_recogida: entry.data['recogida'], Det_pedido.det_modifica: current_user.usu_login, Det_pedido.det_fecha_mod: datetime.now(timezone('America/Bogota'))})
                db.session.commit()
                #Si la entrada es una estola (clase 4)
                if entry.data['clase'] == 4:
                  detalle = Det_pedido.query.filter(Det_pedido.det_clase == 4).order_by(Det_pedido.det_fecha_mod.desc()).first()
                  if form.imagen.data.filename:
                    filename = secure_filename(form.ins_nombre.data + '.jpg')
                    form.imagen.data.save(os.path.join(app.config['UPLOAD_FOLDER'], 'estolas/' +filename))
                  elif Det_estola.query.filter(Det_estola.etl_detalle == detalle.det_id).first().etl_imagen:
                    filename = Det_estola.query.filter(Det_estola.etl_detalle == detalle.det_id).first().etl_imagen
                  else:
                    filename = None
                  Det_estola.query.filter(Det_estola.etl_detalle == detalle.det_id).update({Det_estola.etl_imagen: filename, Det_estola.etl_tipo: form.tipo_estola.data, Det_estola.etl_tipo_escudo: form.tipo_imagen.data , Det_estola.etl_tamano: form.tamano_estola.data , Det_estola.etl_doble_faz: form.doble_faz.data , Det_estola.etl_flequillo: form.flequillo.data, Det_estola.etl_personalizada: form.personalizada.data, Det_estola.etl_terminacion: form.terminacion.data, Det_estola.etl_presentacion: form.presentacion.data, Det_estola.etl_lado_izq: form.lado_izq.data, Det_estola.etl_lado_der: form.lado_der.data, Det_estola.etl_sesgo: form.sesgo.data, Det_estola.etl_sesgo_color: form.sesgo_color.data },synchronize_session=False)
                  db.session.commit()
              #Delete Detalle
              else:
                det_estola = Det_estola.query.filter(Det_estola.etl_detalle == detalle.det_id).first()
                if det_estola:
                  #Delete Estola
                  db.session.delete(det_estola)
                  db.session.commit()
                db.session.delete(detalle)
                db.session.commit()
            else:
              #Create Detalle
              if entry.data['pedida']:
                new_det = Det_pedido(numero, entry.data['clase'], entry.data['color'], entry.data['estilo'], entry.data['detalle'], entry.data['pedida'], entry.data['cortesia'], entry.data['despachada'], entry.data['devuelta'], entry.data['entregada'], entry.data['faltante'], entry.data['recogida'], current_user.usu_login, None)
                db.session.add(new_det)
                db.session.commit()

                if entry.data['clase'] == 4:
                  detalle = Det_pedido.query.filter(Det_pedido.det_clase == 4).order_by(Det_pedido.det_fecha_mod.desc()).first()
                  if form.imagen.data.filename:
                    filename = secure_filename(form.ins_nombre.data + '.jpg')
                    form.imagen.data.save(os.path.join(app.config['UPLOAD_FOLDER'], 'estolas/' +filename))
                  else:
                    filename = None
                  new_est = Det_estola(filename, detalle.det_id, form.tipo_estola.data, form.tipo_imagen.data, form.tamano_estola.data, form.doble_faz.data, form.flequillo.data, form.personalizada.data, form.terminacion.data, form.presentacion.data, form.lado_izq.data, form.lado_der.data, form.sesgo.data, form.sesgo_color.data)
                  db.session.add(new_est)
                  db.session.commit()
    
          #Se ingresaron datos de las ordenes
          if form.orden_entrega_recogida.data == 1 and form.orden_empaque.data == 1:
            #Orden de empaque
            if Despacho.query.filter(Despacho.des_pedido == numero, Despacho.des_prestamo == form.prestamo.data).first():
              #Update empaque
              label['accion'] = 'actualizada'
              Despacho.query.filter(Despacho.des_pedido == numero, Despacho.des_prestamo == form.prestamo.data).update({Despacho.des_presindiv: form.presindiv.data , Despacho.des_prespedido: form.prespedido.data, Despacho.des_fecha_entrega: form.fecha_entrega_des.data, Despacho.des_hora_entrega: text_to_time(form.hora_entrega_des.data), Despacho.des_observaciones: form.observaciones_des.data, Despacho.des_modifica: current_user.usu_login, Despacho.des_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
              db.session.commit()
              des = Despacho.query.order_by(Despacho.des_fecha_mod.desc()).first()
              #Update Orden Entrega/Recogida
              #Orden de entrega
              entrega = Orden.query.filter(Orden.ord_despacho == des.des_id, Orden.ord_tipo == 1).first()
              if entrega.ord_personalizada:  
                tipo_orden = Tipo_orden.query.get(form.ent_tipo_orden.data).tip_tipo
                if tipo_orden == 1:
                  #Update Entrega Personalizada
                  Personalizada.query.filter(Personalizada.per_id == entrega.ord_personalizada).update({Personalizada.per_encargado: form.ent_per_encargado.data, Personalizada.per_cedula: form.ent_per_cedula.data, Personalizada.per_celular: form.ent_per_celular.data, Personalizada.per_direccion: form.ent_per_direccion.data, Personalizada.per_indicaciones: form.ent_per_indicaciones.data, Personalizada.per_municipio: form.ent_per_municipio.data, Personalizada.per_lugar: form.ent_per_lugar.data, Personalizada.per_barrio: form.ent_per_barrio.data, Personalizada.per_repartidores: form.ent_per_repartidores.data, Personalizada.per_cel_repartidor: form.ent_per_cel_repartidor.data}, synchronize_session=False)
                  db.session.commit()
                  per = entrega.ord_personalizada
                  tra = None
                elif tipo_orden == 2:
                  #Create Entrega Transportadora
                  new_tra = Transportadora(form.ent_tra_encargado.data, form.ent_tra_cedula.data, form.ent_tra_municipio.data, form.ent_tra_barrio.data, form.ent_tra_direccion.data, form.ent_tra_indicaciones.data, form.ent_tra_telefono.data, form.ent_tra_empresa.data, form.ent_tra_emp_telefono.data, form.ent_tra_taquilla.data, form.ent_tra_emp_info.data, form.ent_tra_nombre.data, form.ent_tra_celular.data, form.ent_tra_hora.data, form.ent_tra_enc_costos.data)
                  db.session.add(new_tra)
                  db.session.commit()                
                  per = None
                  tra = new_tra.tra_id
              else:
                tipo_orden = Tipo_orden.query.get(form.ent_tipo_orden.data).tip_tipo
                if tipo_orden == 1:
                  #Create Entrega Personalizada
                  new_per = Personalizada(form.ent_per_encargado.data, form.ent_per_cedula.data, form.ent_per_celular.data, form.ent_per_direccion.data, form.ent_per_indicaciones.data, form.ent_per_municipio.data, form.ent_per_lugar.data, form.ent_per_barrio.data, form.ent_per_repartidores.data, form.ent_per_cel_repartidor.data)
                  db.session.add(new_per)
                  db.session.commit()
                  per = new_per.per_id
                  tra = None
                elif tipo_orden == 2:
                  #Update Entrega Transportadora
                  Transportadora.query.filter(Transportadora.tra_id == entrega.ord_transportadora).update({Transportadora.tra_encargado: form.ent_tra_encargado.data, Transportadora.tra_cedula: form.ent_tra_cedula.data, Transportadora.tra_municipio: form.ent_tra_municipio.data, Transportadora.tra_barrio: form.ent_tra_barrio.data, Transportadora.tra_direccion: form.ent_tra_direccion.data, Transportadora.tra_indicaciones: form.ent_tra_indicaciones.data, Transportadora.tra_telefono: form.ent_tra_telefono.data, Transportadora.tra_empresa: form.ent_tra_empresa.data, Transportadora.tra_emp_telefono: form.ent_tra_emp_telefono.data, Transportadora.tra_taquilla: form.ent_tra_taquilla.data, Transportadora.tra_emp_info: form.ent_tra_emp_info.data, Transportadora.tra_nombre: form.ent_tra_nombre.data, Transportadora.tra_celular: form.ent_tra_celular.data, Transportadora.tra_hora: form.ent_tra_hora.data, Transportadora.tra_enc_costos: form.ent_tra_enc_costos.data}, synchronize_session=False)
                  db.session.commit()
                  per = None
                  tra = entrega.ord_transportadora

              Orden.query.filter(Orden.ord_id == entrega.ord_id).update({Orden.ord_fecha: form.ent_fecha.data, Orden.ord_fecha_evento: form.ent_fecha_evento.data, Orden.ord_hora_evento: form.ent_hora_evento.data, Orden.ord_hora: text_to_time(form.ent_hora.data), Orden.ord_personalizada: per, Orden.ord_transportadora: tra, Orden.ord_observaciones: form.ent_observaciones.data, Orden.ord_tipo_orden: form.ent_tipo_orden.data, Orden.ord_modifica: current_user.usu_login, Orden.ord_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
              db.session.commit()

              if tra == None and entrega.ord_transportadora:
                #Delete Entrega Transportadora
                transportadora = Transportadora.query.get(entrega.ord_transportadora)
                db.session.delete(transportadora)
                db.session.commit()
              elif per == None and entrega.ord_personalizada:
                #Delete Entrega Personalizada
                personalizada = Personalizada.query.get(entrega.ord_personalizada)
                db.session.delete(personalizada)
                db.session.commit()

              #Orden de recogida
              recogida = Orden.query.filter(Orden.ord_despacho == des.des_id, Orden.ord_tipo == 2).first()
              if recogida.ord_personalizada:  
                tipo_orden = Tipo_orden.query.get(form.rec_tipo_orden.data).tip_tipo
                if tipo_orden == 1:
                  #Update recogida Personalizada
                  Personalizada.query.filter(Personalizada.per_id == recogida.ord_personalizada).update({Personalizada.per_encargado: form.rec_per_encargado.data, Personalizada.per_cedula: form.rec_per_cedula.data, Personalizada.per_celular: form.rec_per_celular.data, Personalizada.per_direccion: form.rec_per_direccion.data, Personalizada.per_indicaciones: form.rec_per_indicaciones.data, Personalizada.per_municipio: form.rec_per_municipio.data, Personalizada.per_lugar: form.rec_per_lugar.data, Personalizada.per_barrio: form.rec_per_barrio.data, Personalizada.per_repartidores: form.rec_per_repartidores.data, Personalizada.per_cel_repartidor: form.rec_per_cel_repartidor.data}, synchronize_session=False)
                  db.session.commit()
                  per = recogida.ord_personalizada
                  tra = None
                elif tipo_orden == 2:
                  #Create recogida Transportadora
                  new_tra = Transportadora(form.rec_tra_encargado.data, form.rec_tra_cedula.data, form.rec_tra_municipio.data, form.rec_tra_barrio.data, form.rec_tra_direccion.data, form.rec_tra_indicaciones.data, form.rec_tra_telefono.data, form.rec_tra_empresa.data, form.rec_tra_emp_telefono.data, form.rec_tra_taquilla.data, form.rec_tra_emp_info.data, form.rec_tra_nombre.data, form.rec_tra_celular.data, form.rec_tra_hora.data, form.rec_tra_enc_costos.data)
                  db.session.add(new_tra)
                  db.session.commit()                
                  per = None
                  tra = new_tra.tra_id
              else:
                tipo_orden = Tipo_orden.query.get(form.rec_tipo_orden.data).tip_tipo
                if tipo_orden == 1:
                  #Create recogida Personalizada
                  new_per = Personalizada(form.rec_per_encargado.data, form.rec_per_cedula, form.rec_per_celular.data, form.rec_per_direccion.data, form.rec_per_indicaciones.data, form.rec_per_municipio.data, form.rec_per_lugar.data, form.rec_per_barrio.data, form.rec_per_repartidores.data, form.rec_per_cel_repartidor.data)
                  db.session.add(new_per)
                  db.session.commit()
                  per = new_per.per_id
                  tra = None
                elif tipo_orden == 2:
                  #Update recogida Transportadora
                  Transportadora.query.filter(Transportadora.tra_id == recogida.ord_transportadora).update({Transportadora.tra_encargado: form.rec_tra_encargado.data, Transportadora.tra_cedula: form.rec_tra_cedula.data, Transportadora.tra_municipio: form.rec_tra_municipio.data, Transportadora.tra_barrio: form.rec_tra_barrio.data, Transportadora.tra_direccion: form.rec_tra_direccion.data, Transportadora.tra_indicaciones: form.rec_tra_indicaciones.data, Transportadora.tra_telefono: form.rec_tra_telefono.data, Transportadora.tra_empresa: form.rec_tra_empresa.data, Transportadora.tra_emp_telefono: form.rec_tra_emp_telefono.data, Transportadora.tra_taquilla: form.rec_tra_taquilla.data, Transportadora.tra_emp_info: form.rec_tra_emp_info.data, Transportadora.tra_nombre: form.rec_tra_nombre.data, Transportadora.tra_celular: form.rec_tra_celular.data, Transportadora.tra_hora: form.rec_tra_hora.data, Transportadora.tra_enc_costos: form.rec_tra_enc_costos.data}, synchronize_session=False)
                  db.session.commit()
                  per = None
                  tra = recogida.ord_transportadora

              Orden.query.filter(Orden.ord_id == recogida.ord_id).update({Orden.ord_fecha: form.rec_fecha.data, Orden.ord_fecha_evento: form.ent_fecha_evento.data, Orden.ord_hora_evento: form.ent_hora_evento.data, Orden.ord_hora: form.rec_hora.data, Orden.ord_personalizada: per, Orden.ord_transportadora: tra, Orden.ord_observaciones: form.rec_observaciones.data, Orden.ord_tipo_orden: form.rec_tipo_orden.data, Orden.ord_modifica: current_user.usu_login, Orden.ord_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
              db.session.commit()

              if tra == None and recogida.ord_transportadora:
                #Delete Recogida Transportadora
                transportadora = Transportadora.query.get(entrega.ord_transportadora)
                db.session.delete(transportadora)
                db.session.commit()
              elif per == None and recogida.ord_personalizada:
                #Delete Recogida Personalizada
                personalizada = Personalizada.query.get(recogida.ord_personalizada)
                db.session.delete(personalizada)
                db.session.commit()
            else:
              #Create empaque
              label['accion'] = 'ingresada'
              fecha_orden = datetime.now(timezone('America/Bogota'))
              new_des = Despacho(numero, form.prestamo.data, form.presindiv.data, form.prespedido.data, form.fecha_entrega_des.data, text_to_time(form.hora_entrega_des.data), form.observaciones_des.data, fecha_orden, current_user.usu_login, None)
              db.session.add(new_des)
              db.session.commit()

              des = Despacho.query.order_by(Despacho.des_fecha_mod.desc()).first()
              #Create Orden de entrega
              tipo_orden = Tipo_orden.query.get(form.ent_tipo_orden.data).tip_tipo
              if tipo_orden == 1:
                #Entrega Personalizada
                new_per = Personalizada(form.ent_per_encargado.data, form.ent_per_cedula.data, form.ent_per_celular.data, form.ent_per_direccion.data, form.ent_per_indicaciones.data, form.ent_per_municipio.data, form.ent_per_lugar.data, form.ent_per_barrio.data, form.ent_per_repartidores.data, form.ent_per_cel_repartidor.data)
                db.session.add(new_per)
                db.session.commit()

                new_ord = Orden(numero, des.des_id, 1, form.ent_fecha.data, form.ent_fecha_evento.data, form.ent_hora_evento.data, text_to_time(form.ent_hora.data), new_per.per_id, None, form.ent_observaciones.data, form.ent_tipo_orden.data, current_user.usu_login, None)
                db.session.add(new_ord)
                db.session.commit()
              elif tipo_orden == 2:
                #Entrega Transportadora
                new_tra = Transportadora(form.ent_tra_encargado.data, form.ent_tra_cedula.data, form.ent_tra_municipio.data, form.ent_tra_barrio.data, form.ent_tra_direccion.data, form.ent_tra_indicaciones.data, form.ent_tra_telefono.data, form.ent_tra_empresa.data, form.ent_tra_emp_telefono.data, form.ent_tra_taquilla.data, form.ent_tra_emp_info.data, form.ent_tra_nombre.data, form.ent_tra_celular.data, form.ent_tra_hora.data, form.ent_tra_enc_costos.data)
                db.session.add(new_tra)
                db.session.commit()

                new_ord = Orden(numero, des.des_id, 1, form.ent_fecha.data, form.ent_fecha_evento.data, form.ent_hora_evento.data, text_to_time(form.ent_hora.data), None, new_tra.tra_id, form.ent_observaciones.data, form.ent_tipo_orden.data, current_user.usu_login, None)
                db.session.add(new_ord)
                db.session.commit()

              #Create Orden de recogida
              tipo_orden = Tipo_orden.query.get(form.rec_tipo_orden.data).tip_tipo
              if tipo_orden == 1:
                #Recogida Personalizada
                new_per = Personalizada(form.rec_per_encargado.data, form.rec_per_cedula.data, form.rec_per_celular.data, form.rec_per_direccion.data, form.rec_per_indicaciones.data, form.rec_per_municipio.data, form.rec_per_lugar.data, form.rec_per_barrio.data, form.rec_per_repartidores.data, form.rec_per_cel_repartidor.data)
                db.session.add(new_per)
                db.session.commit()

                new_ord = Orden(numero, des.des_id, 2, form.rec_fecha.data, form.ent_fecha_evento.data, form.ent_hora_evento.data, form.rec_hora.data, new_per.per_id, None, form.rec_observaciones.data, form.ent_tipo_orden.data, current_user.usu_login, None)
                db.session.add(new_ord)
                db.session.commit()
              elif tipo_orden == 2:
                #Recogida Transportadora
                new_tra = Transportadora(form.rec_tra_encargado.data, form.rec_tra_cedula.data, form.rec_tra_municipio.data, form.rec_tra_barrio.data, form.rec_tra_direccion.data, form.rec_tra_indicaciones.data, form.rec_tra_telefono.data, form.rec_tra_empresa.data, form.rec_tra_emp_telefono.data, form.rec_tra_taquilla.data, form.rec_tra_emp_info.data, form.rec_tra_nombre.data, form.rec_tra_celular.data, form.rec_tra_hora.data, form.rec_tra_enc_costos.data)
                db.session.add(new_tra)
                db.session.commit()  

                new_ord = Orden(numero, des.des_id, 2, form.rec_fecha.data, form.ent_fecha_evento.data, form.ent_hora_evento.data, form.rec_hora.data, None, new_tra.tra_id, form.rec_observaciones.data, form.ent_tipo_orden.data, current_user.usu_login, None)
                db.session.add(new_ord)
                db.session.commit()

            #Detalles de la orden de empaque
            for i,entry in enumerate(form.tallas.entries):
              detalle = Det_despacho.query.filter(Det_despacho.tal_despacho == des.des_id, Det_despacho.tal_talla == tallas[i].tal_id).first()
              if detalle:
                #Update detalle despacho
                if entry.data['cantidad']:
                  Det_despacho.query.filter(Det_despacho.tal_despacho == des.des_id, Det_despacho.tal_talla == tallas[i].tal_id).update({Det_despacho.tal_cantidad: entry.data['cantidad'], Det_despacho.tal_modifica: current_user.usu_login}, synchronize_session=False)
                  db.session.commit()
                #Delete detalle despacho
                else:
                  db.session.delete(detalle)
                  db.session.commit()
              else:
                #Create detalle despacho
                if entry.data['cantidad']:
                  new_tal = Det_despacho(tallas[i].tal_id, entry.data['cantidad'], des.des_id, current_user.usu_login, None)
                  db.session.add(new_tal)
                  db.session.commit()         

          resumen = [str(form.valor_uni.data), str(form.abonos.data), form.valor_pedido.data, form.valor_despachado.data, form.valor_entregado.data, form.saldo_pedido.data, form.saldo_despachado.data, form.saldo_entregado.data, form.valor_cortesias.data, form.valor_pagar.data, form.saldo_total.data]
          if form.ped_estado_com.data == 1:
            try:
              consecutivo = {}
              consecutivo['pedido'] = numero
              filenames = []
              if request.form['btn'] == 'Grabar pedido' or request.form['btn'] == 'Grabar como pedido/activo' or request.form['btn'] == 'Grabar pedido y enviar copia al cliente':
                if request.form['btn'] == 'Grabar como pedido/activo' or request.form['btn'] == 'Grabar pedido y enviar copia al cliente':
                  enviar = True
                else:
                  enviar = False
                filename = send_pdf(ped.ped_numero, resumen, enviar)
                filenames.append(filename)
                label['concepto'] = 'Pedido'
              elif request.form['btn'] == 'Grabar orden' or request.form['btn'] == 'Grabar orden y enviar copia al cliente':
                if request.form['btn'] == 'Grabar orden y enviar copia al cliente':
                  copia = True
                else:
                  copia = False
                filename = send_pdf_ent_rec(ped.ped_numero, copia)
                filenames.append(filename)
                filename = send_pdf_des(ped.ped_numero, resumen, copia)
                filenames.append(filename)
                filename = send_pdf_letra(ped.ped_numero)
                filenames.append(filename)
                label['concepto'] = 'Orden'
                consecutivo['orden'] = des.des_id
            except Exception as e:
              raise e
              flash(u'Pedido guardado con error al enviar el E-mail: Revisar si se ha cambiado la contraseña del correo recientemente o si se bloqueó la salida del correo por seguridad.', 'warning')
              return redirect('pedidos')
          elif form.ped_estado_com.data == 3:
            flash(u"¡Pedido exitosamente guardado como 'Caído'!", 'success')
            return redirect('pedidos')
          elif form.ped_estado_com.data == 4:
            flash(u"¡Pedido exitosamente guardado como 'Anulado'!", 'success')
            return redirect('pedidos')
            

          #Delete prospecto
          if request.form['btn'] == 'Grabar como pedido/activo':
            prospecto = Prospecto.query.get(request.args.get('prospecto'))
            for detalle in Det_prospecto.query.filter(Det_prospecto.det_prospecto == prospecto.pro_numero):
              if detalle.det_clase == 4:
                estola = Pro_estola.query.filter(Pro_estola.etl_detalle == detalle.det_id).first()
                db.session.delete(estola)
                db.session.commit()
              db.session.delete(detalle)
              db.session.commit()
            db.session.delete(prospecto)
            db.session.commit()

          return render_template("success.html", datos = datos, consecutivo = consecutivo, filenames = filenames, label = label)

    if request.args.get('institucion'):
      institucion = Institucion.query.get(request.args.get('institucion')).serialize
    else:
      institucion = None

    estola = None
    
    if request.args.get('prospecto'):
      prospecto = Prospecto.query.get(request.args.get('prospecto')).serialize
      detalles = []
      for detalle in Det_prospecto.query.filter(Det_prospecto.det_prospecto == request.args.get('prospecto')):
        if detalle.det_clase == 4:
          estola = Pro_estola.query.filter(Pro_estola.etl_detalle == detalle.det_id).first().serialize
        detalles.append(detalle.serialize)
    else:
      prospecto = None
      detalles = []

    return render_template('pedido.html',
                           datos = datos,
                           form = form,
                           clases = clases,
                           tallas = tallas,
                           cedulas = cedulas,
                           ins_data = ins_data,
                           cliente = request.args.get('cliente'),
                           institucion = institucion,
                           prospecto = prospecto,
                           detalles = detalles,
                           estola = estola,
                           pedido = request.args.get('pedido'))

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
  id = request.args.get('id')
  resumen = gen_resumen(id)
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

def gen_resumen(id):
  pedido = Pedido.query.get(id)
  detalle = Det_pedido.query.filter(Det_pedido.det_pedido == id, Det_pedido.det_clase == pedido.ped_principal).first()
  val_unitario = pedido.ped_val_unitario
  abono = pedido.ped_abono
  if not abono: abono = 0
  if detalle:
    valor_pedido = detalle.det_pedida * val_unitario
    valor_despachado = detalle.det_despachada * val_unitario
    valor_entregado = detalle.det_entregada * val_unitario
    valor_cortesias = detalle.det_cortesia * val_unitario
  else:
    valor_pedido = 0
    valor_pedido = 0
    valor_despachado = 0
    valor_entregado = 0
    valor_cortesias = 0
  saldo_pedido = valor_pedido - abono
  if saldo_pedido < 0: saldo_pedido = 0
  saldo_despachado = valor_despachado - abono
  if saldo_despachado < 0: saldo_despachado = 0
  saldo_entregado = valor_entregado - abono
  if saldo_entregado < 0: saldo_entregado = 0
  valor_pagar = valor_entregado - valor_cortesias
  saldo_total = valor_pagar - abono

  if abono == 0: abono = None

  resumen = [val_unitario, abono, valor_pedido, valor_despachado, valor_entregado, saldo_pedido, saldo_despachado, saldo_entregado, valor_cortesias, valor_pagar, saldo_total]

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




