
      # Create/Update del client
        if Cliente.query.get(form.identificacion_enc.data) is None:
          new_cli = Cliente(form.identificacion_enc.data, form.nombre_enc.data, form.municipio_enc.data, form.direccion_enc.data,form.email_enc.data,form.celular_enc.data, form.telefono_enc.data, form.extension_enc.data,form.barrio_enc.data, form.cli_medioConocio.data, form.mes_enc.data, form.dia_enc.data)
          db.session.add(new_cli)
          db.session.commit()
        else:
          Cliente.query.filter(Cliente.cli_identificacion == form.identificacion_enc.data).update({Cliente.cli_nombre: form.nombre_enc.data, Cliente.cli_ciudad: form.municipio_enc.data, Cliente.cli_direccion: form.direccion_enc.data,form.cli_Cliente.cli_medioConocio: form.cli_medioConocio.data, Cliente.cli_nacido_mes: form.mes_enc.data, Cliente.cli_nacido_dia: form.dia_enc.data, Cliente.cli_email: form.email_enc.data, Cliente.cli_celular: form.celular_enc.data, Cliente.cli_telefono: form.telefono_enc.data, Cliente.cli_extension: form.extension_enc.data, Cliente.cli_barrio: form.barrio_enc.data, Cliente.cli_modifica: current_user.usu_login, Cliente.cli_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
          db.session.commit()








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
