import os   
from flask import redirect, render_template, request, flash, url_for, jsonify
from flask.ext.login import login_required
from app import app, db, mail_ext, admin_permission
from flask.ext.wtf import Form
from wtforms import HiddenField
from wtforms.validators import Optional
from app.model.prospecto import Prospecto
from app.model.det_prospecto import Det_prospecto
from app.model.pro_estola import Pro_estola
from app.model.cliente import Cliente
from app.model.institucion import Institucion
from app.model.ciudad import Ciudad


class Input_pro(Form):
    prospecto = HiddenField(validators=[Optional()])

@app.route('/prospectos', methods=['GET', 'POST'])
@login_required
def prospectos():
    datos = {'title' : 'Facturación Casa Luifer'}
    form = Input_pro()
    prospectos = []
    for prospecto in Prospecto.query.order_by(Prospecto.pro_fecha_contacto).all():
        cliente = Cliente.query.get(prospecto.pro_cliente)
        institucion = Institucion.query.get(prospecto.pro_institucion)
        prospectos.append({'cliente': cliente.serialize, 'cli_ciudad': Ciudad.query.get(cliente.cli_ciudad).ciu_nombre, 'institucion': institucion.serialize, 'ins_ciudad': Ciudad.query.get(institucion.ins_ciudad).ciu_nombre, 'fecha_contacto': date_format(prospecto.pro_fecha_contacto), 'id': prospecto.pro_numero})


    if form.validate_on_submit():
        if form.prospecto.data:
            prospecto = Prospecto.query.get(form.prospecto.data)
            return redirect(url_for('pedidos',prospecto = prospecto.pro_numero, institucion = prospecto.pro_institucion, cliente = prospecto.pro_cliente))
        else:
            flash(u'No se ha seleccionado ningun prospecto', 'warning')
            return redirect('prospectos')
    return render_template("prospecto.html", datos = datos, prospectos = prospectos, form = form)

def date_format(date):
    try:
        return date.strftime('%b-%d-%Y')
    except Exception:
        return None

