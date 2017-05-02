from flask.ext.wtf import Form
from wtforms import StringField, DecimalField, FieldList, FormField, SelectField, HiddenField, BooleanField, TextAreaField, RadioField
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import DateField, EmailField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Optional, InputRequired, Required
from flask_wtf import Form
from app.utils import timeRange

class RequiredIf(Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)
        else:
            Optional().__call__(form, field)

class RequiredIfValue(Required):
    
    def __init__(self, other_field_name, value, *args, **kwargs):
        self.other_field_name = other_field_name
        self.value = value
        super(RequiredIfValue, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data) and other_field.data == self.value:
            super(RequiredIfValue, self).__call__(form, field)
        else:
            Optional().__call__(form, field)


class Form_Entry_Detalle(Form):
    check = BooleanField()
    detalle = StringField('detalle', validators=[Optional()])
    clase = HiddenField()
    color = SelectField('color', coerce = int, validators=[RequiredIf('check')])
    estilo = SelectField('estilo', coerce = int, validators=[RequiredIf('check')])
    pedida = StringField('pedida', validators = [RequiredIf('check')])
    cortesia = StringField('cortesia', validators = [Optional()])
    despachada = StringField('despachada', validators = [Optional()])
    devuelta = StringField('devuelta', validators = [Optional()])
    entregada = StringField('entregada', validators = [Optional()])
    faltante = StringField('faltante', validators = [Optional()])
    recogida = StringField('recogida', validators = [Optional()])


class Form_Entry_Talla(Form):
    cantidad = StringField('cantidad', validators=[Optional()])
 
class Form_Pedido(Form):
    # Datos Encargado
    nombre_enc = StringField('nombre', validators=[DataRequired()])
    apellido_enc = StringField('apellido', validators=[DataRequired()])
    identificacion_enc = DecimalField('identificación', validators=[DataRequired()])
    celular_enc = StringField('celular', validators=[DataRequired()])
    email_enc = StringField('email', validators=[DataRequired()])
    direccion_enc = StringField('direccion')
    telefono_enc = StringField('telefono', validators=[Optional()])
    extension_enc = StringField('Ext.', validators=[Optional()])
    mes_enc = SelectField('Mes', coerce = int, choices = [(1, 'Enero'),(2, 'Febrero'),(3, 'Marzo'),(4, 'Abril'),(5, 'Mayo'),(6, 'Junio'),(7, 'Julio'),(8, 'Agosto'),(9, 'Septiembre'),(10, 'Octubre'),(11, 'Noviembre'),(12, 'Diciembre')], validators=[Optional()])
    dia_enc = SelectField('Día', coerce = int, validators=[Optional()])
    barrio_enc = StringField('barrio')    
    cargo_enc = SelectField(coerce = int, validators=[DataRequired()])
    otro_cargo_enc = StringField(validators=[DataRequired()])
    ins_data_check = RadioField('¿Hay datos de la institucion?', coerce = int, choices = [(1,'Si'), (2, 'No')], default = 1, validators = [Optional()])
    municipio_enc = SelectField(coerce = int, validators=[DataRequired()])
    otro_municipio_enc = StringField(validators=[DataRequired()])

    #Datos Institucion
    ins_nit = DecimalField('nit', validators=[Optional()])
    ins_nombre = StringField('nombre institucion', validators=[Optional()])
    ins_ciudad = SelectField(coerce = int, validators=[DataRequired()])
    otro_ins_ciudad = StringField(validators=[DataRequired()])

    #Datos Pedido
    ped_poblacion = SelectField('Poblacion<span class="obligatorio">*</span>', coerce = int, choices = [(1,'Adultos'), (2,'Niños')], validators = [DataRequired()])
    fecha_evento = DateField('fecha_evento', validators=[Optional()])
    hora_evento = TimeField('hora_evento', validators=[Optional()]) 
    fecha_entrega = DateField('Fecha de entrega', validators=[Optional()])
    hora_entrega = SelectField('Hora de entrega', coerce = str, choices = [(t, t) for t in timeRange()], validators=[Optional()])
    fecha_recogida = DateField('Fecha de devolución', validators=[Optional()])
    hora_recogida = TimeField('Hora de devolución', validators=[Optional()])
    tipo_entrega_ord = SelectField('Tipo de entrega<span class="obligatorio">*</span>', coerce = int, validators=[DataRequired()])
    tipo_recogida_ord = SelectField('Tipo de devolución', coerce = int, validators=[Optional()])
    vendedor = SelectField('Vendedor<span class="obligatorio">*</span>', coerce = str, validators = [DataRequired()])
    valor_uni = DecimalField('Valor unitario<span class="obligatorio">*</span>', validators = [DataRequired()]) ## default = 10000
    valor_sugerido = HiddenField(validators=[Optional()], default = 0)

    abonos = DecimalField('Abonos', validators = [Optional()])
    
    ped_evento = SelectField('Tipo de evento', coerce = int, validators=[DataRequired()])
    otro_ped_evento = StringField( validators=[DataRequired()])

    ped_nivele = SelectField('Nivel edu.', coerce = int, validators=[DataRequired()])
    otro_ped_nivele = StringField( validators=[DataRequired()])

    ped_jornada = SelectField('Jornada', coerce = int, validators=[DataRequired()])
    otro_ped_jornada = StringField( validators=[DataRequired()])

    ped_estado_com = SelectField('Estado comercial',coerce = int, validators = [DataRequired()])
    ped_estado_fin = SelectField('Estado financiero',coerce = int, validators = [Optional()])
    ped_estado = SelectField('Estado pedido',coerce = int, validators = [Optional()])

    ped_observacion = TextAreaField('Observaciones')
    fecha_contacto = DateField('Fecha de contacto<span class="obligatorio">*</span>', validators=[RequiredIfValue('ped_estado_com', 2)])

    ped_manual = StringField('Consecutivo', validators=[Optional()])

    #   Detalles del pedido
    id_pedido = StringField(validators=[Optional()])
    principal = RadioField(coerce = int, validators = [InputRequired()])
    tipo_estola = SelectField(coerce = int, validators=[Optional()])
    tipo_imagen = SelectField('Imagen escudo', coerce = int, validators = [RequiredIfValue('tipo_estola', 2)])
    tamano_estola = SelectField('Tamaño de estola', coerce = int, choices = [(1,'Ancha'),(2,'Normal'),(3,'Estrecha')], validators = [RequiredIfValue('tipo_estola', 2)])
    terminacion = SelectField('Terminacion de estola', coerce = int, validators = [RequiredIfValue('tipo_estola', 2)])
    presentacion = SelectField('Presentacion de estola', coerce = int, validators = [RequiredIfValue('tipo_estola', 2)])
    acabado = SelectField('Acabado de estola', coerce = int, validators = [RequiredIfValue('tipo_estola', 2)])
    doble_faz = SelectField('Estola doble faz', coerce = int, choices = [(1,'Si'),(2,'No')], validators = [RequiredIfValue('tipo_estola', 2)])
    flequillo = SelectField('Estola flequillo', coerce = int, choices = [(1,'Si'),(2,'No')], validators = [RequiredIfValue('tipo_estola', 2)])
    personalizada = SelectField('Estola personalizada', coerce = int, choices = [(1,'Si'),(2,'No')], validators = [RequiredIfValue('tipo_estola', 2)])
    lado_izq = StringField('Lado Izq.', validators = [Optional()])
    lado_der = StringField('Lado Der.', validators = [Optional()])
    sesgo = SelectField('Sesgo', coerce = int, choices = [(1,'Si'),(2,'No')], validators = [RequiredIfValue('tipo_estola', 2)])
    sesgo_color = SelectField('Color sesgo', coerce = int, validators = [RequiredIfValue('tipo_estola', 2)])

    imagen = FileField('Imagen', validators=[Optional()])
    detalles = FieldList(FormField(Form_Entry_Detalle), min_entries = 0)

    #Datos de empaque y despacho
    fecha_orden = DateField('Fecha de la orden de empaque', validators=[Optional()])    
    fecha_orden_entrega = DateField('Fecha de la orden de entrega', validators=[Optional()])
    orden_empaque = RadioField(coerce = int, choices = [(1,'Si'), (2, 'No')], validators = [DataRequired()], default = 2)

    tallas = FieldList(FormField(Form_Entry_Talla), min_entries = 0)

    presindiv = SelectField('Presentacion individual de cada toga<span class="obligatorio">*</span>', coerce=int, validators=[RequiredIfValue('orden_empaque', 1)])
    otro_presindiv = StringField( validators=[RequiredIfValue('orden_empaque', 1)])

    prespedido = SelectField('Presentacion general del pedido<span class="obligatorio">*</span>', coerce=int, validators=[RequiredIfValue('orden_empaque', 1)])
    otro_prespedido = StringField( validators=[RequiredIfValue('orden_empaque', 1)])

    prestamo = SelectField('Motivo de la orden<span class="obligatorio">*</span>', coerce=int, validators=[RequiredIfValue('orden_empaque', 1)])
    otro_prestamo = StringField( validators=[RequiredIfValue('orden_empaque', 1)])
    fecha_entrega_des = DateField('Fecha de entrega a despacho<span class="obligatorio">*</span>', validators=[RequiredIfValue('orden_empaque', 1)])
    hora_entrega_des = SelectField('Hora de entrega a despacho', coerce = str, choices = [(t, t) for t in timeRange()], validators=[Optional()])
    observaciones_des = TextAreaField('Observaciones', validators=[Optional()])


    orden_entrega_recogida = RadioField(coerce = int, choices = [(1,'Si'), (2, 'No')], validators = [DataRequired()], default = 2)
    #Datos de la orden de entrega
    ent_fecha = DateField('Fecha de entrega<span class="obligatorio">*</span>', validators=[RequiredIfValue('orden_entrega_recogida', 1)])
    ent_hora = SelectField('Hora de entrega', coerce = str, choices = [(t, t) for t in timeRange()], validators=[Optional()])
    ent_tipo_orden = SelectField('Tipo de entrega<span class="obligatorio">*</span>', coerce = int, validators=[RequiredIfValue('orden_entrega_recogida', 1)])
    ent_observaciones = TextAreaField('Observaciones de la entrega', validators=[Optional()])
    ent_fecha_evento = DateField('Fecha del evento<span class="obligatorio">*</span>', validators=[RequiredIfValue('orden_entrega_recogida', 1)])
    ent_hora_evento = TimeField('Hora del evento', validators=[Optional()])
    #-----Datos de la entrega personalizada
    ent_per_encargado = StringField('Entregar pedido a',validators=[Optional()])
    ent_per_cedula = StringField('C.C.',validators=[Optional()])
    ent_per_celular = StringField('Celular',validators=[Optional()])
    ent_per_direccion = StringField('Direccion',validators=[Optional()])
    ent_per_indicaciones = StringField('Indicaciones',validators=[Optional()])
    ent_per_municipio = SelectField('Municipio',coerce=int,validators=[Optional()])
    otro_ent_per_municipio = StringField(validators=[Optional()])
    ent_per_lugar = StringField('Lugar, auditorio, universidad, colegio, salón, etc', validators=[Optional()])
    ent_per_barrio = StringField('Barrio', validators=[Optional()])
    ent_per_repartidores = StringField('# de repartidores', validators=[Optional()])
    ent_per_cel_repartidor = StringField('Celular del repartidor', validators=[Optional()])
    #-----Datos de la entrega por transportadora
    ent_tra_encargado = StringField('Dirigido a',validators=[Optional()])
    ent_tra_cedula = StringField('C.C. destinatario', validators=[Optional()])
    ent_tra_municipio = SelectField('Municipio de destino',coerce = int,validators=[Optional()])
    otro_ent_tra_municipio = StringField(validators=[Optional()])
    ent_tra_barrio = StringField('Barrio, verda, corregimiento', validators=[Optional()])
    ent_tra_direccion = StringField('Dirección de destino', validators=[Optional()])
    ent_tra_indicaciones = StringField('Indicaciones', validators=[Optional()])
    ent_tra_telefono = StringField('Tel o cel del lugar de destino', validators=[Optional()])
    ent_tra_empresa = StringField('Empresa transportadora', validators=[Optional()])
    ent_tra_emp_telefono = StringField('Telefono de la transportadora',validators=[Optional()])
    ent_tra_taquilla = StringField('No. de taquilla', validators=[Optional()])
    ent_tra_emp_info = StringField('No. ruta/placas/vehiculo/vuelo/etc', validators=[Optional()])
    ent_tra_nombre = StringField('Nombre del conducttor', validators=[Optional()])
    ent_tra_celular = StringField('Celular del coductor', validators=[Optional()])
    ent_tra_hora = TimeField('Hora de salida del transporte', validators=[Optional()])
    ent_tra_enc_costos = StringField('Responsable costos', validators=[Optional()])

    #Datos de la orden de recogida
    rec_fecha = DateField('Fecha de devolución<span class="obligatorio">*</span>', validators=[RequiredIfValue('orden_entrega_recogida', 1)])
    rec_hora = TimeField('Hora de devolución', validators=[Optional()])
    rec_tipo_orden = SelectField('Tipo de devolución<span class="obligatorio">*</span>', coerce = int, validators=[RequiredIfValue('orden_entrega_recogida', 1)])
    rec_observaciones = TextAreaField('Observaciones de la devolución', validators=[Optional()])
    #-----Datos de la recogida personalizada
    rec_per_encargado = StringField('Recoger pedido a',validators=[Optional()])
    rec_per_cedula = StringField('C.C.',validators=[Optional()])
    rec_per_celular = StringField('Celular',validators=[Optional()])
    rec_per_direccion = StringField('Direccion',validators=[Optional()])
    rec_per_indicaciones = StringField('Indicaciones',validators=[Optional()])
    rec_per_municipio = SelectField('Municipio',coerce=int,validators=[Optional()])
    otro_rec_per_municipio = StringField(validators=[Optional()])
    rec_per_lugar = StringField('Lugar, auditorio, universidad, colegio, salón, etc', validators=[Optional()])
    rec_per_barrio = StringField('Barrio', validators=[Optional()])
    rec_per_repartidores = StringField('# de repartidores', validators=[Optional()])
    rec_per_cel_repartidor = StringField('Celular del repartidor', validators=[Optional()])
    #-----Datos de la recogida por transportadora
    rec_tra_encargado = StringField('Dirigido a',validators=[Optional()])
    rec_tra_cedula = StringField('C.C. destinatario', validators=[Optional()])
    rec_tra_municipio = SelectField('Municipio de origen',coerce = int,validators=[Optional()])
    otro_rec_tra_municipio = StringField(validators=[Optional()])
    rec_tra_barrio = StringField('Barrio, verda, corregimiento', validators=[Optional()])
    rec_tra_direccion = StringField('Dirección de origen', validators=[Optional()])
    rec_tra_indicaciones = StringField('Indicaciones', validators=[Optional()])
    rec_tra_telefono = StringField('Tel o cel del lugar de origen', validators=[Optional()])
    rec_tra_empresa = StringField('Empresa transportadora', validators=[Optional()])
    rec_tra_emp_telefono = StringField('Telefono de la transportadora',validators=[Optional()])
    rec_tra_taquilla = StringField('No. de taquilla', validators=[Optional()])
    rec_tra_emp_info = StringField('No. ruta/placas/vehiculo/vuelo/etc', validators=[Optional()])
    rec_tra_nombre = StringField('Nombre del conducttor', validators=[Optional()])
    rec_tra_celular = StringField('Celular del coductor', validators=[Optional()])
    rec_tra_hora = TimeField('Hora de salida del transporte', validators=[Optional()])
    rec_tra_enc_costos = StringField('Responsable costos', validators=[Optional()])


    #Datos usados en la logica del pedido
    suma = HiddenField(default = 0)

    #Resumen del Pedido
    valor_pedido = HiddenField(validators=[Optional()])
    saldo_pedido = HiddenField(validators=[Optional()])
    valor_despachado = HiddenField(validators=[Optional()])
    saldo_despachado = HiddenField(validators=[Optional()])
    valor_entregado = HiddenField(validators=[Optional()])
    saldo_entregado = HiddenField(validators=[Optional()])
    valor_cortesias = HiddenField(validators=[Optional()])
    valor_pagar = HiddenField(validators=[Optional()])
    saldo_total = HiddenField(validators=[Optional()])






        

    
