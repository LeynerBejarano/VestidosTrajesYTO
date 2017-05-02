from flask import render_template, redirect, request, jsonify, flash
from flask.ext.login import login_required, current_user
from flask.ext.wtf import Form
from wtforms.fields.html5 import IntegerField
from wtforms import StringField, DecimalField, SelectField, RadioField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, InputRequired, Optional
from app import app, db
from app.model.accesorio import Accesorio
from app.model.color import Color
from app.model.linea import Linea
from app.model.clase import Clase
from app.model.estilo import Estilo
from app.model.estola import Estola
from app.model.terminacion import Terminacion
from app.model.presentacion import Presentacion
from pytz import timezone
from datetime import datetime


class Input_acc(Form):
    cantidad = IntegerField('cantidad', validators=[InputRequired()])
    nombre = StringField('nombre', validators=[DataRequired()])
    val_unitario = DecimalField('Valor unitario<span class="obligatorio">*</span>', validators=[InputRequired()])
    linea = SelectField('Linea<span class="obligatorio">*</span>', coerce = int, validators=[DataRequired()])
    otro_color = StringField(validators=[DataRequired()])

    ####Estola
    tamano = SelectField('Tamaño', coerce = int, choices = [(1,'Ancha'),(2,'Normal'),(3,'Estrecha')], validators = [Optional()])
    terminacion = SelectField('Terminación', coerce = int, validators = [Optional()])
    presentacion = SelectField('Presentación', coerce = int, validators = [Optional()])
    doble_faz = RadioField(coerce = int, choices = [(1,'Si'),(2,'No')], validators = [Optional()])
    flequillo = RadioField(coerce = int, choices = [(1,'Si'),(2,'No')], validators = [Optional()])


        
# db.create_all()

@app.route('/accesorios', methods=['GET', 'POST'])
@login_required
def input_acc():
    datos = {'title' : 'Facturación Casa Luifer'}
    tipo = 2
    form = Input_acc()
    lineas = [(l.lin_id, l.lin_nombre) for l in Linea.query.order_by(Linea.lin_id)]
    form.linea.choices = lineas

    terminaciones = [(t.ter_id, t.ter_nombre) for t in Terminacion.query.order_by(Terminacion.ter_nombre)]
    form.terminacion.choices = terminaciones
    presentaciones = [(p.prs_id, p.prs_nombre) for p in Presentacion.query.order_by(Presentacion.prs_nombre)]
    form.presentacion.choices = presentaciones

    if form.validate_on_submit():
        color = request.form.get('color')
        if request.form.get('color') == -1:
          new_col = Color(form.otro_color.data, request.form.get('clase'))
          db.session.add(new_col)
          db.session.commit()
          color = Cargo.query.order_by(Cargo.crg_id.desc()).first().crg_id

        if Accesorio.query.filter(Accesorio.acc_clase == request.form.get('clase'), Accesorio.acc_color == color, Accesorio.acc_estilo == request.form.get('estilo')).first():
            Accesorio.query.filter(Accesorio.acc_clase == request.form.get('clase'), Accesorio.acc_color == color, Accesorio.acc_estilo == request.form.get('estilo')).update({Accesorio.acc_nombre: form.nombre.data, Accesorio.acc_cantidad: form.cantidad.data, Accesorio.acc_val_unitario: form.val_unitario.data, Accesorio.acc_modifica: current_user.usu_login, Accesorio.acc_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
            db.session.commit()
            acc = Accesorio.query.order_by(Accesorio.acc_fecha_mod.desc()).first()
            if request.form.get('clase') == 4:
                if Estola.query.get(acc.acc_id):
                    Estola.query.filter(Estola.etl_id == acc.acc_id).update({Estola.etl_id: acc.acc_id, Estola.etl_tamano: form.tamano.data, Estola.etl_doble_faz: form.doble_faz.data, Estola.etl_flequillo: form.flequillo.data, Estola.etl_terminacion: form.terminacion.data, Estola.etl_presentacion: form.presentacion.data}, synchronize_session=False)
                    db.session.commit()
            flash(u'¡Accesorio exitosamente actualizado!', 'success')
        else:
            new_acc = Accesorio(form.nombre.data, request.form.get('linea'), color, request.form.get('estilo'), request.form.get('clase'), form.cantidad.data, form.val_unitario.data, current_user.usu_login, None)        
            db.session.add(new_acc)
            db.session.commit()
            if request.form.get('clase') == 4:
                acc = Accesorio.query.order_by(Accesorio.acc_fecha_mod.desc()).first()
                new_etl = Estola(acc.acc_id, form.tamano.data, form.doble_faz.data, form.flequillo.data, form.terminacion.data, form.presentacion.data)
                db.session.add(new_etl)
                db.session.commit()
            flash(u'¡Accesorio exitosamente creado!', 'success')
        return redirect('accesorios')

    return render_template('accesorios.html',datos= datos, form= form, tipo = tipo)


@app.route('/_cargar_accesorio')
def cargar_accesorio():
    id = request.args.get('id')
    mod = request.args.get('mod')
    accesorio = None
    if not id:
        if int(mod) == 1:
            accesorio = Accesorio.query.order_by(Accesorio.acc_id).first()
        elif int(mod) == -1:
            accesorio = Accesorio.query.order_by(Accesorio.acc_id.desc()).first()
    else:
        if int(mod) == 1:
            accesorio = Accesorio.query.filter(Accesorio.acc_id > id).order_by(Accesorio.acc_id).first()
        elif int(mod) == -1:
            accesorio = Accesorio.query.filter(Accesorio.acc_id < id).order_by(Accesorio.acc_id.desc()).first()

    if accesorio:
        return jsonify(id = accesorio.acc_id, accesorio = accesorio.serialize)
    else:
        return jsonify(id = id)