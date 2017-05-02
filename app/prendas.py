import os
from flask import render_template, redirect, request, jsonify, send_from_directory, flash
from flask.ext.wtf import Form
from wtforms import StringField, DecimalField, SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import IntegerField
from werkzeug import secure_filename
from wtforms.validators import DataRequired, InputRequired, Optional
from app import app, db
from flask.ext.login import login_required, current_user
from app.model.prenda import Prenda
from app.model.color import Color
from app.model.estilo import Estilo
from app.model.clase import Clase
from flask.ext.login import current_user
from app.model.linea import Linea
from pytz import timezone
from datetime import datetime



class Input_pre(Form):
    cantidad = IntegerField('cantidad', validators=[InputRequired()])
    piezas = IntegerField('piezas', validators=[InputRequired()])
    imagen = FileField('imagen', validators=[Optional()])
    nombre = StringField('nombre', validators=[DataRequired()])
    val_unitario = DecimalField('Valor unitario<span class="obligatorio">*</span>', validators=[InputRequired()])
    linea = SelectField('Linea<span class="obligatorio">*</span>', coerce = int, validators=[DataRequired()])
        
# db.create_all()

@app.route('/prendas', methods=['GET', 'POST'])
@login_required
def input_pre():
    datos = {'title' : 'Facturación Casa Luifer'}
    tipo = 1
    form = Input_pre()
    lineas = [(l.lin_id, l.lin_nombre) for l in Linea.query.order_by(Linea.lin_id)]
    form.linea.choices = lineas
   
    if form.validate_on_submit():
        filename = secure_filename(form.imagen.data.filename)
        if filename:
            form.imagen.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        
        if Prenda.query.filter(Prenda.pre_clase == request.form.get('clase'), Prenda.pre_color == request.form.get('color'), Prenda.pre_estilo == request.form.get('estilo')).first():
            imagen = Prenda.query.filter(Prenda.pre_clase == request.form.get('clase'), Prenda.pre_color == request.form.get('color'), Prenda.pre_estilo == request.form.get('estilo')).first()
            if not filename and imagen:
                filename = imagen
            Prenda.query.filter( Prenda.pre_clase == request.form.get('clase'), Prenda.pre_color == request.form.get('color'), Prenda.pre_estilo == request.form.get('estilo')).update({Prenda.pre_nombre: form.nombre.data, Prenda.pre_cantidad: form.cantidad.data, Prenda.pre_piezas: form.piezas.data, Prenda.pre_imagen: filename, Prenda.pre_val_unitario: form.val_unitario.data, Prenda.pre_modifica: current_user.usu_login, Prenda.pre_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
            db.session.commit()
            flash(u'¡Prenda exitosamente actualizada!', 'success')
        else:
            new_pre = Prenda(form.nombre.data, form.cantidad.data, form.piezas.data, request.form.get('color'), request.form.get('clase'), request.form.get('estilo'), request.form.get('linea'), filename, form.val_unitario.data, current_user.usu_login, None)
            db.session.add(new_pre)
            db.session.commit()
            flash(u'¡Prenda exitosamente creada!', 'success')
        return redirect('prendas')

    return render_template('prendas.html',datos= datos, form= form, tipo = tipo)

@app.route('/_cargar_clases')
def cargar_clases():
    id = request.args.get('id')
    tipo = request.args.get('tipo')
    clases = [[clase.cla_id, clase.cla_nombre] for clase in Clase.query.filter(Clase.cla_linea == id, Clase.cla_tipo == tipo)]
    return jsonify(clases = clases)

@app.route('/_cargar_colores_estilos')
def cargar_colores_estilos():
    id = request.args.get('id')
    colores = [[color.col_id, color.col_nombre] for color in Color.query.filter(Color.col_clase == id).order_by(Color.col_nombre)]
    estilos = [[estilo.est_id, estilo.est_nombre] for estilo in Estilo.query.filter(Estilo.est_clase == id).order_by(Estilo.est_nombre)]
    return jsonify(colores = colores, estilos = estilos)

@app.route('/_cargar_prenda')
def cargar_prenda():
    id = request.args.get('id')
    mod = request.args.get('mod')
    prenda = None
    if not id:
        if int(mod) == 1:
            prenda = Prenda.query.order_by(Prenda.pre_id).first()
        elif int(mod) == -1:
            prenda = Prenda.query.order_by(Prenda.pre_id.desc()).first()
    else:
        if int(mod) == 1:
            prenda = Prenda.query.filter(Prenda.pre_id > id).order_by(Prenda.pre_id).first()
        elif int(mod) == -1:
            prenda = Prenda.query.filter(Prenda.pre_id < id).order_by(Prenda.pre_id.desc()).first()

    if prenda:
        return jsonify(id = prenda.pre_id, prenda = prenda.serialize)
    else:
        return jsonify(id = id)



