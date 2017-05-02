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



class Input_cli(Form):
    nombre_enc = StringField('nombre_enc', validators=[DataRequired()])
    apellido_enc = StringField('apellido_enc', validators=[DataRequired()])
    identificacion_enc = DecimalField('identificacion_enc', validators=[DataRequired()])
    celular_enc = StringField('celular_enc', validators=[DataRequired()])
    email_enc = StringField('email_enc', validators=[DataRequired()])
    direccion_enc = StringField('direccion_enc')
    telefono_enc = StringField('telefono_enc', validators=[DataRequired()])
    extension_enc = StringField('Ext.', validators=[DataRequired()])
    mes_enc = SelectField('Mes', coerce = int, choices = [(1, 'Enero'),(2, 'Febrero'),(3, 'Marzo'),(4, 'Abril'),(5, 'Mayo'),(6, 'Junio'),(7, 'Julio'),(8, 'Agosto'),(9, 'Septiembre'),(10, 'Octubre'),(11, 'Noviembre'),(12, 'Diciembre')], validators=[Optional()])
    dia_enc = SelectField('Día', coerce = int, validators=[Optional()])
    barrio_enc = StringField('barrio_enc')    
    cargo_enc = SelectField(coerce = int, validators=[DataRequired()])
    otro_cargo_enc = StringField(validators=[DataRequired()])
    municipio_enc = SelectField(coerce = int, validators=[DataRequired()])
    otro_municipio_enc = StringField(validators=[DataRequired()])

        
# db.create_all()

@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    datos = {'title' : 'Facturación Casa Luifer'}
    form = Input_cli()
    cargos = Cargo.query.order_by(Cargo.crg_descripcion)
    ciudades = Ciudad.query.order_by(Ciudad.ciu_nombre)
    choices = [(c.ciu_id, c.ciu_nombre) for c in ciudades] + [(-1, 'Otro')]
    form.municipio_enc.choices = choices
    choices = [(c.crg_id, c.crg_descripcion) for c in cargos] + [(-1, 'Otro')]
    form.cargo_enc.choices = choices

    #### Creacion de arreglos usados en el auto-completar de jquery
    cedulas = [int(cli.cli_identificacion) for cli in Cliente.query]

    if form.is_submitted():
      form.dia_enc.choices = [(i, str(i)) for i in range(1,32)]
    else:
      form.dia_enc.choices = []

    if form.validate_on_submit():
        if Cliente.query.get(form.identificacion_enc.data) is None:
          new_cli = Cliente(form.identificacion_enc.data, form.nombre_enc.data, form.apellido_enc.data, form.municipio_enc.data, form.direccion_enc.data, form.mes_enc.data, form.dia_enc.data,form.email_enc.data, form.celular_enc.data, form.telefono_enc.data, form.extension_enc.data, form.cargo_enc.data, form.barrio_enc.data, current_user.usu_login, None)
          db.session.add(new_cli)
          db.session.commit()
          if request.form['btn'] == 'Insertar':
            flash(u'¡Cliente exitosamente creado!', 'success')
        else:
          Cliente.query.filter(Cliente.cli_identificacion == form.identificacion_enc.data).update({Cliente.cli_nombre: form.nombre_enc.data, Cliente.cli_apellido: form.apellido_enc.data, Cliente.cli_ciudad: form.municipio_enc.data, Cliente.cli_direccion: form.direccion_enc.data, Cliente.cli_nacido_mes: form.mes_enc.data, Cliente.cli_nacido_dia: form.dia_enc.data, Cliente.cli_email: form.email_enc.data, Cliente.cli_celular: form.celular_enc.data, Cliente.cli_telefono: form.telefono_enc.data, Cliente.cli_extension: form.extension_enc.data, Cliente.cli_cargo: form.cargo_enc.data, Cliente.cli_barrio: form.barrio_enc.data, Cliente.cli_modifica: current_user.usu_login, Cliente.cli_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
          db.session.commit()
          if request.form['btn'] == 'Insertar':
            flash(u'¡Cliente exitosamente actualizado!', 'success')

        if request.form['btn'] == 'Insertar':
          return redirect('clientes')
        else:
          return redirect(url_for('pedidos',cliente = form.identificacion_enc.data))

    return render_template('clientes.html',datos= datos, form= form, cedulas = cedulas)



@app.route('/_cargar_encargado')
def cargar_encargado():
    id = request.args.get('id')
    mod = request.args.get('mod')
    cliente = None
    if not id:
        if int(mod) == 1:
            cliente = Cliente.query.order_by(Cliente.cli_identificacion).first()
        elif int(mod) == -1:
            cliente = Cliente.query.order_by(Cliente.cli_identificacion.desc()).first()
    else:
        if int(mod) == 1:
            cliente = Cliente.query.filter(Cliente.cli_identificacion > id).order_by(Cliente.cli_identificacion).first()
        elif int(mod) == -1:
            cliente = Cliente.query.filter(Cliente.cli_identificacion < id).order_by(Cliente.cli_identificacion.desc()).first()

    if cliente:
        return jsonify(id = float(cliente.cli_identificacion), cliente = cliente.serialize)
    else:
        return jsonify(id = id)




