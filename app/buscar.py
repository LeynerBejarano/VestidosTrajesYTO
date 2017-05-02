import os   
from flask import redirect, render_template, request, url_for, flash, jsonify
from flask.ext.login import login_required
from app import app, db, mail_ext
from flask.ext.wtf import Form
from wtforms import HiddenField, StringField, SelectField
from wtforms.validators import Optional
from app.model.pedido import Pedido
from app.model.det_pedido import Det_pedido
from app.model.det_estola import Det_estola
from app.model.cliente import Cliente
from app.model.institucion import Institucion
from app.model.ciudad import Ciudad
from app.model.jornada import Jornada


class Input_fil(Form):
    pedido = HiddenField(validators=[Optional()])
    consecutivo = StringField('Consecutivo', validators=[Optional()])
    cli_nombre = StringField('Nombre', validators=[Optional()])
    cli_apellido = StringField('Apellido', validators=[Optional()])
    ins_nombre = StringField('Nombre', validators=[Optional()])
    identificacion = StringField('C.C.', validators=[Optional()])
    nit = StringField('Nit', validators=[Optional()])
    cli_ciudad = SelectField('Municipio', coerce = int, validators=[Optional()])
    ins_ciudad = SelectField('Municipio', coerce = int, validators=[Optional()])


@app.route('/buscar', methods=['GET', 'POST'])
@login_required
def buscar():
    datos = {'title' : 'Facturación Casa Luifer'}
    form = Input_fil()
    ciudades = [(c.ciu_id, c.ciu_nombre) for c in Ciudad.query.order_by(Ciudad.ciu_nombre)]
    form.cli_ciudad.choices = ciudades
    form.ins_ciudad.choices = ciudades

    #### Creacion de arreglos usados en el auto-completar de jquery
    cedulas = []
    for cli in Cliente.query:
      cedulas.append(int(cli.cli_identificacion))
     
    if form.validate_on_submit():
        if form.pedido.data:
            if request.form['btn'] == 'Cargar pedido':
                return redirect(url_for('pedidos',pedido = form.pedido.data))
            elif request.form['btn'] == 'Nuevo abono':
                return redirect(url_for('abonos',pedido = form.pedido.data))

        else:
            flash(u'No se ha seleccionado ningun pedido', 'warning')
            return redirect('buscar')
    return render_template("buscar.html", datos = datos, form = form, cedulas = cedulas)

@app.route('/_buscar_pedidos')
def buscar_pedidos():
    consecutivo = request.args.get('consecutivo')
    identificacion = request.args.get('identificacion')
    cli_nombre = request.args.get('cli_nombre')
    cli_apellido = request.args.get('cli_apellido')
    cli_ciudad = request.args.get('cli_ciudad')
    nit = request.args.get('nit')
    ins_nombre = request.args.get('ins_nombre')
    ins_ciudad = request.args.get('ins_ciudad')

    pedidos = []
    if consecutivo:
        pedido = Pedido.query.get(consecutivo)
        if pedido:
            if pedido.ped_poblacion == 1:
                poblacion = 'Adultos'
            else:
                poblacion = 'Niños'
            det_pedido = {'jornada': Jornada.query.get(pedido.ped_jornada).jor_nombre, 'poblacion': poblacion}
            pedidos.append({'pedido': pedido.serialize, 'institucion': Institucion.query.get(pedido.ped_institucion).serialize, 'cliente': Cliente.query.get(pedido.ped_cliente).serialize, 'det_pedido': det_pedido})
            pedidos[-1]['cliente']['ciudad'] = Ciudad.query.get(pedidos[-1]['cliente']['ciudad']).ciu_nombre
            pedidos[-1]['institucion']['ciudad'] = Ciudad.query.get(pedidos[-1]['institucion']['ciudad']).ciu_nombre
            pedidos[-1]['pedido']['fecha'] = pedido.ped_fecha.strftime('%b-%d-%Y %H:%M %p')
    else:
        clientes = []
        if identificacion:
            cliente = Cliente.query.get(identificacion)
            if cliente:
                clientes.append(cliente)
        else:
            if cli_nombre and cli_apellido and cli_ciudad:
                clientes = Cliente.query.filter(Cliente.cli_nombre.like('%'+cli_nombre+'%'), Cliente.cli_apellido.like('%'+cli_apellido+'%'), Cliente.cli_ciudad == cli_ciudad)
            elif cli_nombre and cli_apellido:
                clientes = Cliente.query.filter(Cliente.cli_nombre.like('%'+cli_nombre+'%'), Cliente.cli_apellido.like('%'+cli_apellido+'%'))
            elif cli_nombre and cli_ciudad:
                clientes = Cliente.query.filter(Cliente.cli_nombre.like('%'+cli_nombre+'%'), Cliente.cli_ciudad == cli_ciudad)
            elif cli_apellido and cli_ciudad:
                clientes = Cliente.query.filter(Cliente.cli_apellido.like('%'+cli_apellido+'%'), Cliente.cli_ciudad == cli_ciudad)
            elif cli_nombre:
                clientes = Cliente.query.filter(Cliente.cli_nombre.like('%'+cli_nombre+'%'))
            elif cli_apellido:
                clientes = Cliente.query.filter(Cliente.cli_apellido.like('%'+cli_apellido+'%'))
            elif cli_ciudad:
                clientes = Cliente.query.filter(Cliente.cli_ciudad == cli_ciudad)

        instituciones = []
        if nit:
            instituciones = Institucion.query.filter(Institucion.ins_nit == nit)
        elif ins_nombre:
            instituciones = Institucion.query.filter(Institucion.ins_nombre.like('%'+ins_nombre+'%'))
        elif ins_ciudad:
            instituciones = Institucion.query.filter(Institucion.ins_ciudad == ins_ciudad)

        if clientes and instituciones:
            for cliente in clientes:
                for institucion in instituciones:
                    matches = Pedido.query.filter(Pedido.ped_cliente == cliente.cli_identificacion, Pedido.ped_institucion == institucion.ins_nit).order_by(Pedido.ped_fecha)
                    if matches:
                        for row in matches:
                            if row.ped_poblacion == 1:
                                poblacion = 'Adultos'
                            else:
                                poblacion = 'Niños'
                            det_pedido = {'jornada': Jornada.query.get(row.ped_jornada).jor_nombre, 'poblacion': poblacion}
                            pedidos.append({'pedido': row.serialize, 'institucion': Institucion.query.get(row.ped_institucion).serialize, 'cliente': Cliente.query.get(row.ped_cliente).serialize, 'det_pedido': det_pedido})
                            pedidos[-1]['cliente']['ciudad'] = Ciudad.query.get(pedidos[-1]['cliente']['ciudad']).ciu_nombre
                            pedidos[-1]['institucion']['ciudad'] = Ciudad.query.get(pedidos[-1]['institucion']['ciudad']).ciu_nombre
                            pedidos[-1]['pedido']['fecha'] = row.ped_fecha.strftime('%b-%d-%Y %H:%M %p')
        elif clientes:
            for cliente in clientes:
                matches = Pedido.query.filter(Pedido.ped_cliente == cliente.cli_identificacion).order_by(Pedido.ped_fecha)
                if matches:
                    for row in matches:
                        if row.ped_poblacion == 1:
                            poblacion = 'Adultos'
                        else:
                            poblacion = 'Niños'
                        det_pedido = {'jornada': Jornada.query.get(row.ped_jornada).jor_nombre, 'poblacion': poblacion}
                        pedidos.append({'pedido': row.serialize, 'institucion': Institucion.query.get(row.ped_institucion).serialize, 'cliente': Cliente.query.get(row.ped_cliente).serialize, 'det_pedido': det_pedido})
                        pedidos[-1]['cliente']['ciudad'] = Ciudad.query.get(pedidos[-1]['cliente']['ciudad']).ciu_nombre
                        pedidos[-1]['institucion']['ciudad'] = Ciudad.query.get(pedidos[-1]['institucion']['ciudad']).ciu_nombre
                        pedidos[-1]['pedido']['fecha'] = row.ped_fecha.strftime('%b-%d-%Y %H:%M %p')
        elif instituciones:
            for institucion in instituciones:
                matches = Pedido.query.filter(Pedido.ped_institucion == institucion.ins_id).order_by(Pedido.ped_fecha)
                if matches:
                    for row in matches:
                        if row.ped_poblacion == 1:
                            poblacion = 'Adultos'
                        else:
                            poblacion = 'Niños'
                        det_pedido = {'jornada': Jornada.query.get(row.ped_jornada).jor_nombre, 'poblacion': poblacion}
                        pedidos.append({'pedido': row.serialize, 'institucion': Institucion.query.get(row.ped_institucion).serialize, 'cliente': Cliente.query.get(row.ped_cliente).serialize, 'det_pedido': det_pedido})
                        pedidos[-1]['cliente']['ciudad'] = Ciudad.query.get(pedidos[-1]['cliente']['ciudad']).ciu_nombre
                        pedidos[-1]['institucion']['ciudad'] = Ciudad.query.get(pedidos[-1]['institucion']['ciudad']).ciu_nombre
                        pedidos[-1]['pedido']['fecha'] = row.ped_fecha.strftime('%b-%d-%Y %H:%M %p')
    return jsonify(pedidos = pedidos)

    