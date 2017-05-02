import os
from flask import render_template, redirect, request, jsonify, flash
from flask.ext.wtf import Form
from wtforms import StringField, DecimalField, SelectField
from wtforms.validators import DataRequired
from app import app, db
from flask.ext.login import login_required, current_user
from flask.ext.login import current_user
from app.model.ciudad import Ciudad
from pytz import timezone
from datetime import datetime



class Input_mun(Form):
    municipio = SelectField('Municipio<span class="obligatorio">*</span>', coerce = int, validators=[DataRequired()])
    nombre = StringField('Nombre<span class="obligatorio">*</span>', validators = [DataRequired()])
        
# db.create_all()

@app.route('/municipios', methods=['GET', 'POST'])
@login_required
def municipios():
    datos = {'title' : 'Facturación Casa Luifer'}
    form = Input_mun()
    form.municipio.choices = [(c.ciu_id, c.ciu_nombre) for c in Ciudad.query.order_by(Ciudad.ciu_nombre)]

    if form.validate_on_submit():
        Ciudad.query.filter(Ciudad.ciu_id == form.municipio.data).update({Ciudad.ciu_nombre: form.nombre.data, Ciudad.ciu_modifica: current_user.usu_login, Ciudad.ciu_fecha_mod: datetime.now(timezone('America/Bogota'))}, synchronize_session=False)
        db.session.commit()

        flash(u'¡Municipio exitosamente actualizado!', 'success')
        return redirect('municipios')

    return render_template('municipios.html',datos= datos, form= form)


