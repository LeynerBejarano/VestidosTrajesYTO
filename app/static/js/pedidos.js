var precios = {};
var precio_clase = 0;
var precio_estola = 0;
var precio_entrega = 0;
var precio_am = 0;
var val_unitario;

function autocompletar() {
    var data = cedulas.slice();
    for (var i = data.length - 1; i >= 0; i--) {
        data[i] = String(data[i]);
    }
    $("#identificacion_enc").autocomplete({
        source: data,
        change: function() {
            $(this).trigger('change');
            if ($.inArray(parseInt($(this).val()), cedulas) >= 0) {
                $.getJSON($SCRIPT_ROOT + '/_cargar_cliente', {
                    id: $(this).val()
                }, function(data) {
                    $("#nombre_enc").val(data.nombre).trigger('change');
                    $("#apellido_enc").val(data.apellido).trigger('change');
                    $("#celular_enc").val(data.celular).trigger('change');
                    $("#telefono_enc").val(data.telefono).trigger('change');
                    $("#extension_enc").val(data.extension).trigger('change');
                    $("#barrio_enc").val(data.barrio).trigger('change');
                    $("#email_enc").val(data.email).trigger('change');
                    $("#direccion_enc").val(data.direccion).trigger('change');
                    $("#cargo_enc").val(data.cargo).trigger('change');
                    $("#municipio_enc").val(data.municipio).trigger('change');
                    if (data.mes != null) {
                        $("#mes_enc").val(data.mes).trigger('change', [data.dia]);
                    }
                    $("#tipo_enc").val("ANTIGUO").trigger('change');
                });
                return false;
            } else {
                $("#tipo_enc").val("NUEVO").trigger('change');
            }
        }
    });
}

function grabarPedido(){
    $('#orden_empaque-1').trigger('click');
    $('#orden_entrega_recogida-1').trigger('click');
}

function grabarOrden(){
    $('#orden_empaque-0').trigger('click');
    $('#orden_entrega_recogida-0').trigger('click');
}


////Copiar datos del encargado

function copiarDatos() {
    $('#ins_ciudad').val($('#municipio_enc').val()).trigger('change');
    $('#ins_direccion').val($('#direccion_enc').val()).trigger('change');
    $('#ins_telefono').val($('#telefono_enc').val()).trigger('change');
    $('#ins_extension').val($('#extension_enc').val()).trigger('change');
    $('#ins_celular').val($('#celular_enc').val()).trigger('change');
    $('#ins_barrio').val($('#barrio_enc').val()).trigger('change');
    $('#ins_correo').val($('#email_enc').val()).trigger('change');
}

////Copiar datos de la entrega

function copiarEntrega() {
    $('#rec_tipo_orden').val($('#ent_tipo_orden').val()).trigger('change');
    $('#rec_per_encargado').val($('#ent_per_encargado').val()).trigger('change');
    $('#rec_per_cedula').val($('#ent_per_cedula').val()).trigger('change');
    $('#rec_per_celular').val($('#ent_per_celular').val()).trigger('change');
    $('#rec_per_direccion').val($('#ent_per_direccion').val()).trigger('change');
    $('#rec_per_indicaciones').val($('#ent_per_indicaciones').val()).trigger('change');
    $('#rec_per_municipio').val($('#ent_per_municipio').val()).trigger('change');
    $('#rec_per_lugar').val($('#ent_per_lugar').val()).trigger('change');
    $('#rec_per_barrio').val($('#ent_per_barrio').val()).trigger('change');
    $('#rec_per_repartidores').val($('#ent_per_repartidores').val()).trigger('change');
    $('#rec_per_cel_repartidor').val($('#ent_per_cel_repartidor').val()).trigger('change');
    $('#rec_tra_encargado').val($('#ent_tra_encargado').val()).trigger('change');
    $('#rec_tra_cedula').val($('#ent_tra_cedula').val()).trigger('change');
    $('#rec_tra_municipio').val($('#ent_tra_municipio').val()).trigger('change');
    $('#rec_tra_barrio').val($('#ent_tra_barrio').val()).trigger('change');
    $('#rec_tra_direccion').val($('#ent_tra_direccion').val()).trigger('change');
    $('#rec_tra_indicaciones').val($('#ent_tra_indicaciones').val()).trigger('change');
    $('#rec_tra_telefono').val($('#ent_tra_telefono').val()).trigger('change');
    $('#rec_tra_empresa').val($('#ent_tra_empresa').val()).trigger('change');
    $('#rec_tra_emp_telefono').val($('#ent_tra_emp_telefono').val()).trigger('change');
    $('#rec_tra_taquilla').val($('#ent_tra_taquilla').val()).trigger('change');
    $('#rec_tra_emp_info').val($('#ent_tra_emp_info').val()).trigger('change');
    $('#rec_tra_nombre').val($('#ent_tra_nombre').val()).trigger('change');
    $('#rec_tra_celular').val($('#ent_tra_celular').val()).trigger('change');
    $('#rec_tra_hora').val($('#ent_tra_hora').val()).trigger('change');
    $('#rec_tra_enc_costos').val($('#ent_tra_enc_costos').val()).trigger('change');
}

function copiarEncargadoEntrega() {
    $('#ent_per_encargado').val($('#nombre_enc').val() + ' ' + $('#apellido_enc').val()).trigger('change');
    $('#ent_per_cedula').val($('#identificacion_enc').val()).trigger('change');
    $('#ent_per_celular').val($('#celular_enc').val()).trigger('change');
    $('#ent_per_direccion').val($('#direccion_enc').val()).trigger('change');
    $('#ent_per_municipio').val($('#municipio_enc').val()).trigger('change');
    $('#ent_per_barrio').val($('#barrio_enc').val()).trigger('change');
    $('#ent_tra_encargado').val($('#nombre_enc').val() + ' ' + $('#apellido_enc').val()).trigger('change');
    $('#ent_tra_cedula').val($('#identificacion_enc').val()).trigger('change');
    $('#ent_tra_municipio').val($('#municipio_enc').val()).trigger('change');
    $('#ent_tra_barrio').val($('#barrio_enc').val()).trigger('change');
    $('#ent_tra_direccion').val($('#direccion_enc').val()).trigger('change');
    $('#ent_tra_telefono').val($('#telefono_enc').val()).trigger('change');
}

function copiarEncargadoRecogida() {
    $('#rec_per_encargado').val($('#nombre_enc').val() + ' ' + $('#apellido_enc').val()).trigger('change');
    $('#rec_per_cedula').val($('#identificacion_enc').val()).trigger('change');
    $('#rec_per_celular').val($('#celular_enc').val()).trigger('change');
    $('#rec_per_direccion').val($('#direccion_enc').val()).trigger('change');
    $('#rec_per_municipio').val($('#municipio_enc').val()).trigger('change');
    $('#rec_per_barrio').val($('#barrio_enc').val()).trigger('change');
    $('#rec_tra_encargado').val($('#nombre_enc').val() + ' ' + $('#apellido_enc').val()).trigger('change');
    $('#rec_tra_cedula').val($('#identificacion_enc').val()).trigger('change');
    $('#rec_tra_municipio').val($('#municipio_enc').val()).trigger('change');
    $('#rec_tra_barrio').val($('#barrio_enc').val()).trigger('change');
    $('#rec_tra_direccion').val($('#direccion_enc').val()).trigger('change');
    $('#rec_tra_telefono').val($('#telefono_enc').val()).trigger('change');
}
////Cargar datos del prospecto

function cargar_prospecto(institucion, prospecto, detalles) {
    $(document).ready(function() {
        ////Cargar institucion
        $("#ins_nombre").val(institucion.nombre);
        $("#ins_nit").val(institucion.nit);
        $("#ins_ciudad").val(institucion.ciudad).trigger('change');

        ///Cargar detalles del prospecto
        $('input[type="checkbox"]:checked').trigger('click');
        for (var i = 0; i < detalles.length; i++) {
            var det_id = detalles[i].clase - 1;
            $('#'.concat(det_id)).prop('checked', true).triggerHandler('click', [null]);
            if (detalles[i].color != null) {
                $('#detalles-'.concat(det_id).concat('-color')).val(detalles[i].color).trigger('change', [null]);
            }

            if (detalles[i].estilo != null) {
                $('#detalles-'.concat(det_id).concat('-estilo')).val(detalles[i].estilo).trigger('change');
            }

            $('#detalles-'.concat(det_id).concat('-detalle')).val(detalles[i].detalle);
            $('#detalles-'.concat(det_id).concat('-pedida')).val(detalles[i].pedida);
            $('#detalles-'.concat(det_id).concat('-cortesia')).val(detalles[i].cortesia);            
            $('#detalles-'.concat(det_id).concat('-despachada')).val(detalles[i].despachada);
            $('#detalles-'.concat(det_id).concat('-devuelta')).val(detalles[i].devuelta);
            $('#detalles-'.concat(det_id).concat('-entregada')).val(detalles[i].entregada);
            $('#detalles-'.concat(det_id).concat('-faltante')).val(detalles[i].faltante);
            $('#detalles-'.concat(det_id).concat('-recogida')).val(detalles[i].recogida);

            //// Cargar estola
            if (String(detalles[i].clase) == '4') {
                if (detalles[i].estilo != null) {
                    $('#acabado').val(detalles[i].estilo).trigger('change');
                }

                if (estola.tipo != null) {
                    $('#tipo_estola').val(estola.tipo).trigger('change', [null]);
                }
                if (estola.tamano != null) {
                    $('#tamano_estola').val(estola.tamano).trigger('change');
                }
                if (estola.terminacion != null) {
                    $('#terminacion').val(estola.terminacion).trigger('change');
                }
                if (estola.presentacion != null) {
                    $('#presentacion').val(estola.presentacion).trigger('change');
                }
                if (estola.imagen != null) {
                    $('#filename').text(estola.imagen);
                }
                $("#tipo_imagen").val(estola.tipo_escudo).trigger('change');
                if (estola.doble_faz != null){
                    $("#doble_faz").val(estola.doble_faz).trigger('change');
                }
                if (estola.flequillo != null){
                    $("#flequillo").val(estola.flequillo).trigger('change');
                }
                if (estola.personalizada != null){
                    $("#personalizada").val(estola.personalizada).trigger('change');
                }
                if (estola.lado_izq != null){
                    $("#lado_izq").val(estola.lado_izq).trigger('change');
                }
                if (estola.lado_der != null){
                    $("#lado_der").val(estola.lado_der).trigger('change');
                }
                if (estola.sesgo != null){
                    $("#sesgo").val(estola.sesgo).trigger('change');
                }
                if (estola.sesgo_color != null){
                    $("#sesgo_color").val(estola.sesgo_color).trigger('change');
                }
            }
        }

        ///Cargar prospecto
        $('#tipo').val(prospecto.tipo).trigger('change');
        $("input[name='principal'][value='"+ (prospecto.principal - 1) +"']").trigger('click');
        $('#ped_poblacion').val(prospecto.poblacion).trigger('change');
        $('#ped_evento').val(prospecto.evento).trigger('change');
        $('#ped_jornada').val(prospecto.jornada).trigger('change');
        $('#ped_nivele').val(prospecto.nivel).trigger('change');
        $('#fecha_evento').val(prospecto.fecha_evento).trigger('change');
        if (prospecto.hora_evento != null) {
            $('#hora_evento').val(prospecto.hora_evento.replace(/:\d\d([ ap]|$)/, '$1')).trigger('change');
        }
        $('#fecha_entrega').val(prospecto.fecha_entrega).trigger('change');
        if (prospecto.hora_entrega != null) {
            $('#hora_entrega').val(prospecto.hora_entrega).trigger('change');
        }
        $('#fecha_recogida').val(prospecto.fecha_recogida).trigger('change');
        if (prospecto.hora_recogida != null) {
            $('#hora_recogida').val(prospecto.hora_recogida.replace(/:\d\d([ ap]|$)/, '$1')).trigger('change');
        }
        $('#vendedor').val(prospecto.vendedor).trigger('change');
        $('#abonos').val(prospecto.abono);
        $('#ped_estado_com').val("1").trigger('change');
        $('#ped_observacion').val(prospecto.observacion);
        $('#tipo_entrega_ord').val(prospecto.tipo_entrega_ord).trigger('change');
        $('#tipo_recogida_ord').val(prospecto.tipo_recogida_ord).trigger('change'); 
        $('#valor_uni').val(prospecto.val_unitario).trigger('change', [null]);

        $('input, select').each(function() {
            if ($(this).val() == '' || $(this).val() == null) {
                $(this).addClass('empty');
            } else {
                $(this).removeClass('empty');
            }
        });
    });
}



jQuery.fn.extend({
    /////////Funcion para verificar checkbox, y des/habilitar campos de los detalles del pedido.
    validar: function(sum) {
        if ($(this).is(':checked')) {
            $('#detalles-'.concat(($(this).attr('id'))).concat('-color')).prop("disabled", false);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-estilo')).prop("disabled", false);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-detalle')).prop("disabled", false);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-pedida')).prop("disabled", false);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-cortesia')).prop("disabled", false);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-devuelta')).prop("disabled", false);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-faltante')).prop("disabled", false);
            if ($(this).attr('id') == 3) {
                $('#tipo_estola').prop("disabled", false);
            }
            if (sum != 0) {
                $('#detalles-'.concat(($(this).attr('id'))).concat('-despachada')).val(sum);
            }
            $('#detalles-'.concat(($(this).attr('id'))).concat('-pedida')).val($('#detalles-0-pedida').val()).trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-cortesia')).val($('#detalles-0-cortesia').val()).trigger('change');
        } else {
            $('#detalles-'.concat(($(this).attr('id'))).concat('-color')).prop("disabled", true);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-estilo')).prop("disabled", true);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-detalle')).prop("disabled", true);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-pedida')).prop("disabled", true);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-cortesia')).prop("disabled", true);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-devuelta')).prop("disabled", true);
            $('#detalles-'.concat(($(this).attr('id'))).concat('-faltante')).prop("disabled", true);
            if ($(this).attr('id') == 3) {
                $('#tipo_estola').prop("disabled", true);
            }
            $('#detalles-'.concat(($(this).attr('id'))).concat('-color')).val('-').trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-estilo')).val('-').trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-detalle')).val(null).trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-pedida')).val(null).trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-cortesia')).val(null).trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-despachada')).val(null).trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-devuelta')).val(null).trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-entregada')).val(null).trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-faltante')).val(null).trigger('change');
            $('#detalles-'.concat(($(this).attr('id'))).concat('-recogida')).val(null).trigger('change');
        }
    }
});

var id = null;
function cargar_pedido(data) {
    id = data.id;
    if (id == null || id == '') {
        $('.siguiente').addClass('disabled');
        $('.anterior').addClass('disabled');
        $("#id_pedido").prop('disabled', true);
    } else {
        ///Limpiar formulario
        $('input[type="checkbox"]:checked').each(function() {
            $(this).trigger('click');
        });
        $('form').trigger("reset");
        $('#dia_enc').empty().append('<option selected disabled>-</option>');
        $('#total-despacho').empty();
        $('#descargarPDF-despacho, #descargarPDF-entrega-recogida').prop('disabled', true); 
        // $('select[id$="estilo"]').each(function() {
        //     $(this).empty().append('<option selected disabled>-</option>');
        // });
        precio_clase = 0;
        precio_estola = 0;
        precio_entrega = 0;
        precio_am = 0;
        precios = {};


        $('#id_pedido').prop('disabled', false);
        $('#id_pedido').val(id).trigger('change', [null]);
    }

    ////Cargar encargardo
    if (typeof data.cliente != 'undefined') {
        $('#identificacion_enc').val(data.cliente);
        $("#identificacion_enc").data("ui-autocomplete")._trigger("change");
    }
    ////Cargar institucion
    if (typeof data.institucion != 'undefined') {
        $("#ins_nombre").val(data.institucion.nombre);
        $("#ins_nit").val(data.institucion.nit);
        $("#ins_ciudad").val(data.institucion.ciudad).trigger('change');
    }

    ///Cargar detalles del pedido
    if (typeof data.detalles != 'undefined') {
        for (var i = 0; i < data.detalles.length; i++) {
            var det_id = data.detalles[i].clase - 1;
            $('#'.concat(det_id)).prop('checked', true).triggerHandler('click', [null]);
            if (data.detalles[i].color != null) {
                $('#detalles-'.concat(det_id).concat('-color')).val(data.detalles[i].color).trigger('change', [null]);
            }

            if (data.detalles[i].estilo != null) {
                $('#detalles-'.concat(det_id).concat('-estilo')).val(data.detalles[i].estilo).trigger('change', [null]);
            }

            $('#detalles-'.concat(det_id).concat('-detalle')).val(data.detalles[i].detalle);
            $('#detalles-'.concat(det_id).concat('-pedida')).val(data.detalles[i].pedida);
            if (data.permiso == false){
                $('#detalles-'.concat(det_id).concat('-pedida')).attr('readonly', true);
            }
            $('#detalles-'.concat(det_id).concat('-cortesia')).val(data.detalles[i].cortesia);
            $('#detalles-'.concat(det_id).concat('-despachada')).val(data.detalles[i].despachada);
            $('#detalles-'.concat(det_id).concat('-devuelta')).val(data.detalles[i].devuelta);
            $('#detalles-'.concat(det_id).concat('-entregada')).val(data.detalles[i].entregada);
            $('#detalles-'.concat(det_id).concat('-faltante')).val(data.detalles[i].faltante);
            $('#detalles-'.concat(det_id).concat('-recogida')).val(data.detalles[i].recogida);

            //// Cargar estola
            if (String(data.detalles[i].clase) == '4') {
                if (data.detalles[i].estilo != null) {
                    $('#acabado').val(data.detalles[i].estilo).trigger('change');
                }

                if (data.estola.tipo != null) {
                    $('#tipo_estola').val(data.estola.tipo).trigger('change', [null]);
                }
                if (data.estola.tamano != null) {
                    $('#tamano_estola').val(data.estola.tamano).trigger('change');
                }
                if (data.estola.terminacion != null) {
                    $('#terminacion').val(data.estola.terminacion).trigger('change');
                }
                if (data.estola.presentacion != null) {
                    $('#presentacion').val(data.estola.presentacion).trigger('change');
                }
                if (data.estola.imagen != null) {
                    $('#filename').text(data.estola.imagen);
                }
                $("#tipo_imagen").val(data.estola.tipo_escudo).trigger('change');
                if (data.estola.doble_faz != null){
                    $("#doble_faz").val(data.estola.doble_faz).trigger('change');
                }
                if (data.estola.flequillo != null){
                    $("#flequillo").val(data.estola.flequillo).trigger('change');
                }
                if (data.estola.personalizada != null){
                    $("#personalizada").val(data.estola.personalizada).trigger('change');
                }

                if (data.estola.lado_izq != null){
                    $("#lado_izq").val(data.estola.lado_izq).trigger('change');
                }
                if (data.estola.lado_der != null){
                    $("#lado_der").val(data.estola.lado_der).trigger('change');
                }
                if (data.estola.sesgo != null){
                    $("#sesgo").val(data.estola.sesgo).trigger('change');
                }
                if (data.estola.sesgo_color != null){
                    $("#sesgo_color").val(data.estola.sesgo_color).trigger('change');
                }
            }
        }
    }

    ///Cargar pedido
    if (typeof data.pedido != 'undefined') {
        $('#tipo').val(data.pedido.tipo).trigger('change');
        $("input[name='principal'][value='"+ (data.pedido.principal - 1) +"']").trigger('click');
        $('#ped_poblacion').val(data.pedido.poblacion).trigger('change');
        $('#ped_evento').val(data.pedido.evento).trigger('change');
        $('#ped_jornada').val(data.pedido.jornada).trigger('change');
        $('#ped_nivele').val(data.pedido.nivel).trigger('change');
        $('#fecha_evento').val(data.pedido.fecha_evento).trigger('change', [null]);
        if (data.pedido.hora_evento != null) {
            $('#hora_evento').val(data.pedido.hora_evento.replace(/:\d\d([ ap]|$)/, '$1')).trigger('change');
        }
        $('#fecha_entrega').val(data.pedido.fecha_entrega).trigger('change', [data.pedido.hora_entrega, null]);
        $('#fecha_recogida').val(data.pedido.fecha_recogida).trigger('change');
        if (data.pedido.hora_recogida != null) {
            $('#hora_recogida').val(data.pedido.hora_recogida.replace(/:\d\d([ ap]|$)/, '$1')).trigger('change');
        }
        $('#vendedor').val(data.pedido.vendedor).trigger('change');
        $('#abonos').val(data.pedido.abono);
        if (data.pedido.estado_com != null) {
            $('#ped_estado_com').val(data.pedido.estado_com).trigger('change');
        }
        $('#ped_observacion').val(data.pedido.observacion);
        if (data.pedido.manual != 0) {
            $('#ped_manual').val(data.pedido.manual);
        }
        $('#tipo_entrega_ord').val(data.pedido.tipo_entrega_ord).trigger('change'); 
        $('#tipo_recogida_ord').val(data.pedido.tipo_recogida_ord).trigger('change'); 
        $('#valor_uni').val(data.pedido.val_unitario).trigger('change', [null]);
        if (data.permiso == false){
            $('#valor_uni').attr('readonly', true);
        }
        $('#fecha-pedido').text(data.pedido.fecha.slice(0, 10))
    }

    cargar_abonos();

    $('input, select').each(function() {
        if ($(this).val() == '' || $(this).val() == null) {
            $(this).addClass('empty');
        } else {
            $(this).removeClass('empty');
        }
    });
}

function cargar_abonos(){
    $.getJSON($SCRIPT_ROOT + '/_cargar_abonos', {
        id: $('#id_pedido').val()
    }, function(data) {
        console.log(data);
        var html = '';
        if (data.abonos.length > 0){
            for (var i = 0; i < data.abonos.length; i++) {
                html += '<tr>' +
                        '<td>' + data.abonos[i].id + '</td>' +
                        '<td>' + data.abonos[i].valor + '</td>' +
                        '<td>' + data.abonos[i].tipo + '</td>' +
                        '<td>' + (data.abonos[i].fecha ? data.abonos[i].fecha: '') + '</td>' +
                        '</tr>';
            }
        } else{
            html = '<tr><td colspan="4" class="text-center">No hay abonos</td></tr>'
        }
        $('#tabla-abonos tbody').html(html);
        $('#tabla-abonos').show();
    });
}


$(document).ready(function() {
    /////////////  Cargar Datos del pedido
    if ($('#id_pedido').val() != '') {
        id = $('#id_pedido').val();
        $('.siguiente').removeClass('disabled');
        $('#id_pedido').prop('disabled', false);
    }


    //Navegar entre pedidos

    $('.siguiente').click(function() {
        if (!$(this).hasClass('disabled')) {
            $('.anterior').removeClass('disabled');
            $.getJSON($SCRIPT_ROOT + '/_cargar_pedido', {
                mod: 1,
                id: id
            }, function(data) {
                if (String(id) == String(data.id)) {
                    $('.siguiente').addClass('disabled');
                } else {
                    cargar_pedido(data);
                }
            });
            return false;
        }
    });

    $('.anterior').click(function() {
        if (!$(this).hasClass('disabled')) {
            $('.siguiente').removeClass('disabled');
            $.getJSON($SCRIPT_ROOT + '/_cargar_pedido', {
                mod: -1,
                id: id
            }, function(data) {
                if (String(id) == String(data.id)) {
                    $('.anterior').addClass('disabled');
                } else {
                    cargar_pedido(data);
                }
            });
            return false;
        }
    });

    $('#id_pedido').change(function(event, flag) {
        if (typeof flag == 'undefined') {
            $.getJSON($SCRIPT_ROOT + '/_cargar_pedido', {
                mod: 0,
                id: $(this).val()
            }, function(data) {
                if (typeof data.pedido != 'undefined') {
                    $('.siguiente').removeClass('disabled');
                    $('.anterior').removeClass('disabled');
                    cargar_pedido(data);
                } else {
                    $('#modal_error_pedido .alert').text('Error: pedido no encontrado');
                    $('#modal_error_pedido').modal();
                    $('#id_pedido').val(id);
                }
            });
            return false;
        }
    });


    ///Obtener dias del mes seleccionado
    $("#mes_enc").change(function(event, dia) {
        $.getJSON($SCRIPT_ROOT + '/_cargar_dias', {
            mes: $(this).val()
        }, function(data) {
            $('#dia_enc').empty();
            $.each(data.choices, function(index, value) {
                $('#dia_enc').append('<option value="' + value[0] + '">' + value[1] + '</option>');
            });
            if (typeof dia != 'undefined') {
                $('#dia_enc').val(dia);
            }
        });
        return false;
    });


    /// Mostrar / Ocultar campos 'otro'

    $('select.other').each(function() {
        if ($(this).val() != -1) {
            $('#otro_'.concat($(this).attr('id'))).hide();
        }
    });

    $('select.other').change(function() {
        if ($(this).val() == -1) {
            $('#otro_'.concat($(this).attr('id'))).val(null);
            $('#otro_'.concat($(this).attr('id'))).show();
        } else {
            $('#otro_'.concat($(this).attr('id'))).val($(this).val());
            $('#otro_'.concat($(this).attr('id'))).hide();
        }
    });


    var sum = parseInt($('#suma').val());

    /////Habilitar campos en caso de haber fallado validacion
    $('input[type=checkbox]').each(function() {
        $(this).validar(sum);
    });

    ////Suma de numero de togas para guardarla en las casillas de despachadas
    $('#num_togas .form-control').change(function() {
        sum = 0;
        $('#num_togas .form-control').each(function() {
            if ($(this).val() != '') {
                sum += parseInt($(this).val());
            }
        });

        $('#suma').val(sum);

        if ($('#prestamo').val() == 5) {
            $('input[type=checkbox]').each(function() {
                if ($(this).is(':checked')) {
                    if (sum != 0) {
                        $('#detalles-'.concat(($(this).attr('id'))).concat('-despachada')).val(sum);
                    } else {
                        $('#detalles-'.concat(($(this).attr('id'))).concat('-despachada')).val(null);
                    }
                    $('#detalles-'.concat(($(this).attr('id'))).concat('-despachada')).trigger('change');
                }
            });
        }

        $('#total-despacho').text(sum);
    });



    //Llamado de la funcion validar de los checkbox al darles click, al seleccionar habilitan y al deseleccionar deshabilitan los campos del detalle
    $('input[type=checkbox]').each(function() {
        $(this).click(function() {
            $(this).validar(sum);
        });
    });

    // Icono de los acordeones

    $('a.btn-block ').on('click', function() {
        $(this).find('span').toggleClass('glyphicon-chevron-down glyphicon-chevron-up');
    });


    // Definir area metropolitana (AM) a partir del valor seleccionado en el municipio
    //PARA EL ENCARGADO
    $('#municipio_enc').change(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_area', {
            id: $(this).val()
        }, function(data) {
            if (data.area == 1) {
                $('#area_enc').text('AM');
            } else if (data.area == 0) {
                $('#area_enc').text('FAM');
            }
        });
        return false;
    });

    $('#municipio_enc').trigger('change');

    // Definir area metropolitana (AM) a partir del valor seleccionado en el municipio
    //PARA LA INSTITUCION
    $('#ins_ciudad').change(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_area', {
            id: $(this).val()
        }, function(data) {
            if (data.area == 1) {
                $('#ins_area').text('AM').triggerHandler('change_am');
            } else if (data.area == 0) {
                $('#ins_area').text('FAM').triggerHandler('change_am');
            }
        });
        return false;
    });

    $('#ins_ciudad').trigger('change');

    // Activar modal para sugerir la oferta de estolas al seleccionar togas

    $('#detalles-0-color').change(function(event, flag) {
        if (typeof flag == 'undefined' && $(this).val() != null) {
            $('#modal_sugerencia').modal();
        }
    });



    // Activar modal de estolas dependiendo de si su tipo es venta o arriendo
    //En caso de venta activar tambien boton
    $('#tipo_estola').change(function(event, flag) {
        if ($(this).val() == 2) {
            if (typeof flag == 'undefined') {
                $('#modal_form').modal();
            }
        } else {
            if ($(this).val() == 1) {
                if (typeof flag == 'undefined') {
                    $('#modal_estolas').modal({
                        escapeClose: false,
                        backdrop: "static"
                    });
                }
            }
        }
    });


    if ($('#3').is(':checked') && $('#tipo_estola').val() == 2) {
        $('#btn-estola').toggleClass("disabled active");
    }

    $('#3').click(function() {
        if (!$(this).is(':checked')) {
            $('#btn-estola').addClass('disabled');
            $('#btn-estola').removeClass('active');
        } else if ($('#tipo_estola').val() == 2) {
            $('#btn-estola').toggleClass("disabled active");
        }
    });

    $('#btn-estola').click(function(event, flag) {
        if (typeof flag == 'undefined') {
            $('#modal_form').modal();
        }
    });


    /// Calculo del valor unitario dependiendo de la toga seleccionada y de los 'accesorios' añadidos, donde los accesorios son las clases mayores o iguales a 5.

    $("#val_sugerido").change(function() {
        if ($(this).text() == 0) {
            $(this).text('');
        } else {
            $('#valor_sugerido').val($(this).text());
            $(this).text('$' + parseFloat($(this).text()).toLocaleString('de-DE'));
        }
    });

    $('#val_sugerido').trigger('change');
    /// Valor de la Toga
    $("select[id$='color'], select[id$='estilo']").change(function() {
        var id = $(this).attr('id').substr(9, 1);
        var clase = $('#detalles-'.concat(id).concat('-clase')).val();
        var color = $('#detalles-'.concat(id).concat('-color')).val();
        var estilo = $('#detalles-'.concat(id).concat('-estilo')).val();
        if (color != null && estilo != null) {
            $.getJSON($SCRIPT_ROOT + '/_cargar_val_unitario', {
                clase: clase,
                color: color,
                estilo: estilo
            }, function(data) {
                if (typeof precios[clase] != 'undefined') {
                    precio_clase -= precios[clase];
                }
                precios[clase] = data.val_unitario;
                precio_clase += precios[clase];
                val_unitario = precio_clase + precio_estola + precio_entrega + precio_am;
                $("#val_sugerido").text(val_unitario).trigger('change');
            });
            return false;
        }
    });

    $("select[id$='color'], select[id$='estilo']").trigger('change', [null]);

    $('input[name$="-check"').click(function() {
        var id = $(this).attr('id');
        var clase = $('#detalles-'.concat(id).concat('-clase')).val();
        if (!$(this).is(':checked')) {
            if (typeof precios[clase] != 'undefined') {
                precio_clase -= precios[clase];
                precios[clase] = 0;
                val_unitario = precio_clase + precio_estola + precio_entrega + precio_am;
                $("#val_sugerido").text(val_unitario).trigger('change');
            }
        }
    });

    //Valor area metropolitana, CUIDADO: valores quemados en el codigo.

    $('#ins_area').bind('change_am', function() {
        if ($(this).text() == 'FAM') {
            precio_am = 5000;
        } else {
            precio_am = 0;
        }
        val_unitario = precio_clase + precio_estola + precio_entrega + precio_am;
        $("#val_sugerido").text(val_unitario).trigger('change');
    });


    // Valor del domicilio

    $("#tipo_entrega_ord").change(function() {
        asfas = $(this).val();
        if ($(this).val() != null) {
            $.getJSON($SCRIPT_ROOT + '/_cargar_val_entrega', {
                id: $(this).val()
            }, function(data) {
                precio_entrega = data.val_unitario;
                val_unitario = precio_clase + precio_estola + precio_entrega + precio_am;
                $("#val_sugerido").text(val_unitario).trigger('change');
            });
            return false;
        }
    });

    $("#tipo_entrega_ord").trigger('change');


    // Valor de la estola

    $("#tipo_imagen").change(function() {
        var id = $(this).val();
        if (id != null) {
            $.getJSON($SCRIPT_ROOT + '/_cargar_val_estola', {
                id: id
            }, function(data) {
                precio_estola = data.val_unitario;
                val_unitario = precio_clase + precio_estola + precio_entrega + precio_am;
                $("#val_sugerido").text(val_unitario).trigger('change');
            });
            return false;
        } else {
            precio_estola = 0;
            val_unitario = precio_clase + precio_estola + precio_entrega + precio_am;
            $("#val_sugerido").text(val_unitario).trigger('change');
        }
    });

    $("#tipo_imagen").trigger('change');

    $('#3').click(function() {
        if (!$(this).is(':checked') || $("#tipo_estola").val() != 2) {
            precio_estola = 0;
            val_unitario = precio_clase + precio_estola + precio_entrega + precio_am;
            $("#val_sugerido").text(val_unitario).trigger('change');
        } else {
            $("#tipo_imagen").trigger('change');
        }
    });

    $("#tipo_estola").change(function() {
        if ($(this).val() == 1) {
            precio_estola = 0;
            val_unitario = precio_clase + precio_estola + precio_entrega + precio_am;
            $("#val_sugerido").text(val_unitario).trigger('change');
        } else {
            $("#tipo_imagen").trigger('change');
        }
    });




    // Duplicar valores de la toga
    $('#detalles-0-pedida').change(function() {
        var cant = $(this).val();
        $('input[type=checkbox]').not(this).each(function() {
            if ($(this).is(':checked')) {
                $('#detalles-'.concat(($(this).attr('id'))).concat('-pedida')).val(cant);
                if (cant == '') {
                    $('#detalles-'.concat(($(this).attr('id'))).concat('-pedida')).addClass('empty');
                } else {
                    $('#detalles-'.concat(($(this).attr('id'))).concat('-pedida')).removeClass('empty');
                }
            }
        });
    });


    ////CUIDADO: duplicar color en birrete, BASADO en su contenido NO en su valor
    $('#detalles-0-color').change(function() {
        if ($('#1').is(':checked') && $('#detalles-1-color').val() == null) {
            $('#detalles-1-color option')
                .filter(function(index) {
                    return $(this).text() === $('#detalles-0-color option:selected').text();
                })
                .prop('selected', true).trigger('change');
        }
    });

    ////CUIDADO: duplicar color de estola en borla, BASADO en su contenido NO en su valor
    $('#detalles-3-color').change(function() {
        if ($('#2').is(':checked') && $('#detalles-2-color').val() == null) {
            $('#detalles-2-color option')
                .filter(function(index) {
                    return $(this).text() === $('#detalles-3-color option:selected').text();
                })
                .prop('selected', true).trigger('change');
        }
    });

    $('#detalles-0-cortesia').change(function() {
        var cant = $(this).val();
        $('input[type=checkbox]').not(this).each(function() {
            if ($(this).is(':checked')) {
                $('#detalles-'.concat(($(this).attr('id'))).concat('-cortesia')).val(cant);
                if (cant == '') {
                    $('#detalles-'.concat(($(this).attr('id'))).concat('-cortesia')).addClass('empty');
                } else {
                    $('#detalles-'.concat(($(this).attr('id'))).concat('-cortesia')).removeClass('empty');
                }
            }
        });
    });


    // Disparadores para calcular valores y saldos      

    $('#valor_pedido').trigger('change');
    $('#saldo_pedido').trigger('change')
    $('#valor_despachado').trigger('change');
    $('#saldo_despachado').trigger('change');
    $('#valor_cortesias').trigger('change');

    $('#detalles-0-pedida').change(function() {
        var cant = parseInt($(this).val());
        var valor = cant * parseFloat($('#valor_uni').val());
        if (!isNaN(valor)) {
            $('#valor_pedido').val(valor);
            $('#valor_pedido').trigger('change');
            $('#saldo_pedido').val(valor);
            $('#saldo_pedido').trigger('change');
        } else {
            $('#valor_pedido').val(null);
            $('#valor_pedido').trigger('change');
            $('#saldo_pedido').val(null);
            $('#saldo_pedido').trigger('change');
        }
    });

    $('#valor_pedido').change(function() {
        $('#valor-pedido').text($(this).val());
    });

    $('#saldo_pedido').change(function() {
        var saldo = parseInt($(this).val()) - parseFloat($('#abonos').val());
        if (isNaN(saldo)) {
            $('#saldo-pedido').text($(this).val());
        } else {
            $(this).val(saldo);
            $('#saldo-pedido').text(saldo);
        }
    });

    $('#detalles-0-despachada').change(function() {
        var val_ped = parseInt($(this).val()) * parseFloat($('#valor_uni').val());
        if (!isNaN(val_ped)) {
            $('#valor_despachado').val(val_ped);
            $('#valor_despachado').trigger('change');
            $('#saldo_despachado').val(val_ped);
            $('#saldo_despachado').trigger('change');
        } else {
            $('#valor_despachado').val(null);
            $('#valor_despachado').trigger('change');
            $('#saldo_despachado').val(null);
            $('#saldo_despachado').trigger('change');
        }
    });


    $('#valor_despachado').change(function() {
        if ($(this).val() != null) {
            $('#valor-despachado').text($(this).val());
        }
    });

    $('#saldo_despachado').change(function() {
        var saldo = parseInt($(this).val()) - parseFloat($('#abonos').val());
        if (isNaN(saldo)) {
            $('#saldo-despachado').text($(this).val());
        } else {
            $(this).val(saldo);
            $('#saldo-despachado').text(saldo);
        }
    });


    $('#detalles-0-cortesia').change(function() {
        var cant = parseInt($(this).val());
        var valor = cant * parseFloat($('#valor_uni').val());
        if (!isNaN(valor)) {
            $('#valor_cortesias').val(valor);
            $('#valor_cortesias').trigger("change");
        } else {
            $('#valor_cortesias').val(null);
            $('#valor_cortesias').trigger("change");
        }
    });

    $('#valor_cortesias').change(function() {
        $('#valor-cortesias').text($(this).val());
    });

    $('#0').click(function(event, flag) {
        if (!$(this).is(':checked')) {
            $('#valor_pedido').val(null);
            $('#valor_pedido').trigger('change');
            $('#saldo_pedido').val(null);
            $('#saldo_pedido').trigger('change');
            $('#valor_despachado').val(null);
            $('#valor_despachado').trigger('change');
            $('#saldo_despachado').val(null);
            $('#saldo_despachado').trigger('change');
            $('#valor_cortesias').val(null);
            $('#valor_cortesias').trigger('change');
        } else {
            $('#detalles-0-despachada').trigger('change');
        }
    });

    $('#valor_uni').change(function() {
        var cant = parseInt($('#detalles-0-pedida').val());
        var valor = cant * parseFloat($(this).val());
        if (!isNaN(valor)) {
            $('#valor_pedido').val(valor).trigger('change');
            $('#saldo_pedido').val(valor).trigger('change');
        } else {
            $('#valor_pedido').val(null).trigger('change');
            $('#saldo_pedido').val(null).trigger('change');
        }

        var cant = parseInt($('#detalles-0-despachada').val());
        var valor = cant * parseFloat($(this).val());
        if (!isNaN(valor)) {
            $('#valor_despachado').val(valor).trigger('change');
            $('#saldo_despachado').val(valor).trigger('change');
        } else {
            $('#valor_despachado').val(null).trigger('change');
            $('#saldo_despachado').val(null).trigger('change');
        }

        var cant = parseInt($('#detalles-0-cortesia').val());
        var valor = cant * parseFloat($(this).val());
        if (!isNaN(valor)) {
            $('#valor_cortesias').val(valor).trigger('change');
        } else {
            $('#valor_cortesias').val(null).trigger('change');
        }
    });

    $('#abonos').change(function() {
        $('#saldo_pedido').val($('#valor_pedido').val()).trigger('change');
        $('#saldo_despachado').val($('#valor_despachado').val()).trigger('change');
    });

    //Show Loader

    $('input[type="submit"]').click(function() {
        $('.loader').show();
    });

    $(window).bind('beforeunload', function() {
        $('.loader').show();
    });

    $('input, select').each(function() {
        if ($(this).val() == '' || $(this).val() == null) {
            $(this).addClass('empty');
        }
    });

    $('input, select').change(function() {
        if ($(this).val() == '' || $(this).val() == null) {
            $(this).addClass('empty');
        } else {
            $(this).removeClass('empty');
        }
    });

    ////Mostrar/ocultar fecha de contacto

    $('#contacto').hide();
    $('#ped_estado_com').change(function() {
        if ($(this).val() == '2') {
            $('#contacto').show();
        } else {
            $('#contacto').hide();
        }
    });

    $('#ped_estado_com').trigger('change');

    $('#cargo_enc').change(function() {
        if ($(this).val() == 11 || $(this).val() == 12) {
            $('#ins_data_check').show();
        } else {
            $("input[name='ins_data_check'][value='1']").trigger('click');
            $('#ins_data_check').hide();
        }
    });

    $('input[name="ins_data_check"]:radio').change(function() {
        if ($('input[name="ins_data_check"]:checked').val() == 2) {
            $('#ins_nombre').val('uncaught');
            $('#ins_nit').val(0);
            $('#ins_ciudad').val(1).trigger('change');
            $('#panel_ins').hide();
        } else {
            $('#ins_nombre').val(null);
            $('#ins_nit').val(null);
            $('#ins_ciudad').val('-').trigger('change');
            $('#panel_ins').show();
        }
    });


    /////Habilitar/Deshabilitar campos de la estola

    if ($('#3').is(':checked')) {
        $('#acabado').prop('disabled', false);
        $('#tamano_estola').prop('disabled', false);
        $('#terminacion').prop('disabled', false);
        $('#presentacion').prop('disabled', false);
        $('#doble_faz').prop('disabled', false);
        $('#flequillo').prop('disabled', false);
        $('#personalizada').prop('disabled', false);
        $('#tipo_imagen').prop('disabled', false);
        $('#lado_izq').prop('disabled', false);
        $('#lado_der').prop('disabled', false);
        $('#sesgo').prop('disabled', false);
        $('#sesgo_color').prop('disabled', false);
    }

    $('#3').click(function() {
        if ($(this).is(':checked')) {
            $('#acabado').prop('disabled', false);
            $('#tamano_estola').prop('disabled', false);
            $('#terminacion').prop('disabled', false);
            $('#presentacion').prop('disabled', false);
            $('#doble_faz').prop('disabled', false);
            $('#flequillo').prop('disabled', false);
            $('#personalizada').prop('disabled', false);
            $('#tipo_imagen').prop('disabled', false);
            $('#lado_izq').prop('disabled', false);
            $('#lado_der').prop('disabled', false);
            $('#sesgo').prop('disabled', false);
            $('#sesgo_color').prop('disabled', false);
        } else {
            $('#acabado').prop('disabled', true);
            $('#tamano_estola').prop('disabled', true);
            $('#terminacion').prop('disabled', true);
            $('#presentacion').prop('disabled', true);
            $('#doble_faz').prop('disabled', true);
            $('#flequillo').prop('disabled', true);
            $('#personalizada').prop('disabled', true);
            $('#tipo_imagen').prop('disabled', true);
            $('#lado_izq').prop('disabled', true);
            $('#lado_der').prop('disabled', true);
            $('#sesgo').prop('disabled', true);
            $('#sesgo_color').prop('disabled', true);
            //Borrar datos de estolas deseleccionadas
            $('#acabado').val('-').trigger('change');
            $('#tipo_estola').val('-').trigger('change');
            $('#tamano_estola').val('-').trigger('change');
            $('#terminacion').val('-').trigger('change');
            $('#presentacion').val('-').trigger('change');
            $('#sesgo').val('-').trigger('change');
            $('#sesgo_color').val('-').trigger('change');
            $('#doble_faz').val('-').trigger('change');
            $('#flequillo').val('-').trigger('change');
            $('#personalizada').val('-').trigger('change');
            $('#tipo_imagen').val('-').trigger('change');
            $('#lado_izq').val('').trigger('change');
            $('#lado_der').val('').trigger('change');
        }
    });


    //// Mostrar cantidad de prendas/accesorios disponibles

    $('#fecha_evento').change(function() {
        if ($(this).val() != '') {
            $('.disponible').show();
            $('input[type="checkbox"]:checked').each(function() {
                var id = $(this).attr('id');
                $.getJSON($SCRIPT_ROOT + '/_cargar_disponible', {
                    fecha: $('#fecha_evento').val(),
                    color: $('#detalles-' + id + '-color').val(),
                    estilo: $('#detalles-' + id + '-estilo').val(),
                    clase: $('#detalles-' + id + '-clase').val()
                }, function(data) {
                    $('#' + id).siblings('span.disponible').text(data.cantidad);
                });
            });
        } else {
            $('.disponible').hide();
        }
    });

    $('#fecha_evento').trigger('change');


    ///Seleccionar tipo de entrega dependiendo de la cantidad pedida

    $('#detalles-0-pedida').change(function() {
        if ($(this).val() <= 50) {
            $('#tipo_entrega_ord').val(1).trigger('change');
        }
    });


    ///Mostrar ocultar estilo de la estola
    $('.estilo-estola').hide();
    if ($('#tipo_estola').val() == 2) {
        $('.estilo-estola').show();
        $('td.row-adjustable').prop('rowspan', '5');
        $('.col-adjustable').removeProp('colspan');
    }

    $('#tipo_estola').change(function() {
        if ($(this).val() == 1) {
            $('.estilo-estola').hide();
            $('td.row-adjustable').removeProp('rowspan');
            $('.col-adjustable').prop('colspan', '2');
        } else if ($(this).val() == 2) {
            $('.estilo-estola').show();
            $('td.row-adjustable').prop('rowspan', '5');
            $('.col-adjustable').removeProp('colspan');
        }
    });

    ///Duplicar valor de acabado
    $('#acabado').change(function() {
        $('#detalles-3-estilo').val($(this).val()).trigger('change');
    });



    ///Agragar valor a estilo de estola si el tipo es alquiler
    $('#tipo_estola').change(function() {
        if ($(this).val() == 1) {
            $('#acabado').val('17').trigger('change');
        }
    });

    ///Mostrar/Ocultar tipo de orden de entrega
    $('#ent_tipo_orden, #rec_tipo_orden').change(function() {
        if ($(this).val() != null) {
            var prefix = $(this).attr('id').slice(0, 3);
            var tipo_orden = $(this).val();

            $.getJSON($SCRIPT_ROOT + '/_cargar_tipo_orden', {
                id: $(this).val()
            }, function(data) {
                if (data.tipo == 1) {
                    $('#' + prefix + '_personalizada').show();
                    $('#' + prefix + '_transportadora').hide();
                    if (tipo_orden == 1) {
                        $('div.' + prefix + '-per-ins').hide();
                    } else {
                        $('div.' + prefix + '-per-ins').show();
                    }
                } else if (data.tipo == 2) {
                    $('#' + prefix + '_transportadora').show();
                    $('#' + prefix + '_personalizada').hide();
                }
            });
        }
    });

    $('#ent_tipo_orden, #rec_tipo_orden').trigger('change');

    ///Quitar attr required de las horas para poder validar en el servidor
    $('#rec_hora, #ent_hora_evento').removeAttr('required');

    ///Mostrar nombre de la imagen seleccionada
    $('#imagen').change(function() {
        if ($('#imagen')[0].files[0]) {
            $('#filename').text($('#imagen')[0].files[0].name);
        } else {
            $('#filename').text('Ningún archivo seleccionado');
        }
    });

    $('#imagen').trigger('change');


    ///Descargar pdf del pedido

    $('#id_pedido').change(function() {
        if ($(this).val() != '') {
            $('#descargarPDF').prop('disabled', false);
        } else {
            $('#descargarPDF').prop('disabled', true);
        }
    });

    $('#descargarPDF').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_descargar_pdf', {
            id: $('#id_pedido').val()
        }, function(data) {
            window.open("uploads/pedido.pdf");
        });
    });

    ///Descargar pdf de la orden de empaque y despacho

    $('#descargarPDF-despacho').click(function() {
        $(".loader").show();
        $.getJSON($SCRIPT_ROOT + '/_descargar_pdf_despacho', {
            id: $('#id_pedido').val(),
            id_motivo: $('#prestamo').val()
        }, function(data) {
            window.open("uploads/orden_despacho.pdf");
        });
        $(".loader").hide();
    });

    ///Descargar pdf de la orden de entrega y recogida

    $('#descargarPDF-entrega-recogida').click(function() {
        $(".loader").show();
        $.getJSON($SCRIPT_ROOT + '/_descargar_pdf_entrega_recogida', {
            id: $('#id_pedido').val(),
            id_motivo: $('#prestamo').val()
        }, function(data) {
            window.open("uploads/orden_entrega_recogida.pdf");
        });
        $(".loader").hide();
    });



    //// Cargar horas al cambiar fecha de entrega y fecha de entrega a despacho
    $('#fecha_entrega_des').change(function(event, hora) {
        if (typeof hora != 'undefined') {
            var actual = hora;
        } else {
            var actual = null;
        }
        $.getJSON($SCRIPT_ROOT + '/_cargar_horas_entrega_des', {
            fecha: $(this).val(),
            hora: actual
        }, function(data) {
            $('#hora_entrega_des').empty();
            $.each(data.horas, function(index, value) {
                $('#hora_entrega_des').append('<option value="' + value + '">' + value + '</option>');
            });
            $('#hora_entrega_des').append('<option selected disabled>-</option>');
            if (actual) {
                $('#hora_entrega_des').val(actual).trigger('change');
            }
        });
    });

    $('#ent_fecha').change(function(event, hora) {
        if (typeof hora != 'undefined') {
            var actual = hora;
        } else {
            var actual = null;
        }
        $.getJSON($SCRIPT_ROOT + '/_cargar_horas_entrega', {
            fecha: $(this).val(),
            hora: actual
        }, function(data) {
            $('#ent_hora').empty();
            $.each(data.horas, function(index, value) {
                $('#ent_hora').append('<option value="' + value + '">' + value + '</option>');
            });
            $('#ent_hora').append('<option selected disabled>-</option>');
            if (actual) {
                $('#ent_hora').val(actual).trigger('change');
            }
        });
    });

    $('#fecha_entrega').change(function(event, hora) {
        if (typeof hora != 'undefined') {
            var actual = hora;
        } else {
            var actual = null;
        }
        $.getJSON($SCRIPT_ROOT + '/_cargar_horas_entrega', {
            fecha: $(this).val(),
            hora: actual
        }, function(data) {
            $('#hora_entrega').empty();
            $.each(data.horas, function(index, value) {
                $('#hora_entrega').append('<option value="' + value + '">' + value + '</option>');
            });
            $('#hora_entrega').append('<option selected disabled>-</option>');
            if (actual) {
                $('#hora_entrega').val(actual).trigger('change');
            }
        });
    });

    /// Autocompletar fechas de entrega y recogida dependiendo de la fecha de entrega

    $("#fecha_evento").change(function(event, flag) {
        if (typeof flag == 'undefined'){
            $.getJSON($SCRIPT_ROOT + '/_obtener_fechas', {
                fecha_evento: $(this).val(),
                ciudad: $("#ins_ciudad").val()
            }, function(data) {
                if (data.flag == true) {
                    $('#fecha_entrega').val(data.fecha_entrega).trigger('change');
                    $('#fecha_recogida').val(data.fecha_recogida).trigger('change');
                }
            });
        }
    });

    $("#ent_fecha_evento").change(function(event, flag) {
        if (typeof flag == 'undefined'){
            $.getJSON($SCRIPT_ROOT + '/_obtener_fechas', {
                fecha_evento: $(this).val(),
                ciudad: $("#ins_ciudad").val()
            }, function(data) {
                if (data.flag == true) {
                    $('#ent_fecha').val(data.fecha_entrega).trigger('change');
                    $('#rec_fecha').val(data.fecha_recogida).trigger('change');
                }
            });
        }
    });

    $("#fecha_entrega, #ent_fecha").change(function(event, flag1, flag2) {
        if (typeof flag1 == 'undefined' || typeof flag2 != 'undefined' ) {
            $.getJSON($SCRIPT_ROOT + '/_obtener_fecha_despacho', {
                fecha_entrega: $(this).val()
            }, function(data) {
                if (data.flag == true) {
                    $('#fecha_entrega_des').val(data.fecha_despacho).trigger('change');
                }
            });
        }
    });

    // Copiar fechas entre pedido y ordenes

    $("#fecha_evento").change(function() {
        if ($(this).val() != null && $(this).val() != '') {
            $('#ent_fecha_evento').val($(this).val()).removeClass('empty');
        }
    });

    $("#fecha_entrega").change(function() {
        if ($(this).val() != null && $(this).val() != '') {
            $('#ent_fecha').val($(this).val()).removeClass('empty');
        }
    });

    $("#fecha_recogida").change(function() {
        if ($(this).val() != null && $(this).val() != '') {
            $('#rec_fecha').val($(this).val()).removeClass('empty');
        }
    });

    $("#ent_fecha_evento").change(function() {
        if ($(this).val() != null && $(this).val() != '' && $('#prestamo').val() == 5) {
            $('#fecha_evento').val($(this).val()).removeClass('empty');
        }
    });

    $("#ent_fecha").change(function() {
        if ($(this).val() != null && $(this).val() != '' && $('#prestamo').val() == 5) {
            $('#fecha_entrega').val($(this).val()).removeClass('empty');
        }
    });

    $("#rec_fecha").change(function() {
        if ($(this).val() != null && $(this).val() != '' && $('#prestamo').val() == 5) {
            $('#fecha_recogida').val($(this).val()).removeClass('empty');
        }
    });

    ///Copiar horas entre pedido y ordenes

    $("#hora_evento").change(function() {
        if ($(this).val() != null && $(this).val() != '') {
            $('#ent_hora_evento').val($(this).val()).removeClass('empty');
        }
    });

    $("#hora_entrega").change(function() {
        if ($(this).val() != null && $(this).val() != '') {
            $('#ent_hora').val($(this).val()).removeClass('empty');
        }
    });

    $("#hora_recogida").change(function() {
        if ($(this).val() != null && $(this).val() != '') {
            $('#rec_hora').val($(this).val()).removeClass('empty');
        }
    });

    $("#ent_hora_evento").change(function() {
        if ($(this).val() != null && $(this).val() != '' && $('#prestamo').val() == 5) {
            $('#hora_evento').val($(this).val()).removeClass('empty');
        }
    });

    $("#ent_hora").change(function() {
        if ($(this).val() != null && $(this).val() != '' && $('#prestamo').val() == 5) {
            $('#hora_entrega').val($(this).val()).removeClass('empty');
        }
    });

    $("#rec_hora").change(function() {
        if ($(this).val() != null && $(this).val() != '' && $('#prestamo').val() == 5) {
            $('#hora_recogida').val($(this).val()).removeClass('empty');
        }
    });

    /// Cargar orden
    $('#prestamo').change(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_orden', {
            id_motivo: $(this).val(),
            id_pedido: $("#id_pedido").val()
        }, function(data) {
            $('#orden_empaque select, #orden_entrega_recogida select').not('#prestamo, #ent_hora, #hora_entrega_des, #ent_tipo_orden, #rec_tipo_orden').val('-').addClass('empty');
            $('#orden_empaque input[type="text"], #orden_entrega_recogida input[type="text"]').not('#otro_prestamo').val(null).addClass('empty');
            $('#orden_empaque textarea, #orden_entrega_recogida textarea').empty(); 
            $('#total-despacho').empty();
            if (data.flag == true) {
                //Cargar orden de despacho

                $('#presindiv').val(data.despacho.presindiv).trigger('change');
                $('#prespedido').val(data.despacho.prespedido).trigger('change');
                $('#fecha_entrega_des').val(data.despacho.fecha_entrega).trigger('change', [data.despacho.hora_entrega]);

                ////Cargar detalles del despacho
                for (var i = 0; i < data.detalles.length; i++) {
                    var index = $('#tallas td').filter(function() {
                        return $(this).text() == data.detalles[i].talla;
                    }).first().index() - 1;

                    $('#cantidad td:eq(' + index + ') input').val(data.detalles[i].cantidad).trigger('change');
                }

                //Cargar orden de entrega y recogida
                //Orden de entrega
                $("input[name='orden_entrega_recogida'][value='1']").trigger('click');
                $('#ent_fecha').val(data.entrega.fecha).trigger('change', [data.entrega.hora]);
                $('#ent_tipo_orden').val(data.entrega.tipo_orden).trigger('change');
                $('#ent_observaciones').val(data.entrega.observaciones).trigger('change');
                $('#ent_fecha_evento').val(data.entrega.fecha_evento).trigger('change', [null]);
                if (data.entrega.hora_evento) {
                    $('#ent_hora_evento').val(data.entrega.hora_evento.replace(/:\d\d([ ap]|$)/, '$1')).trigger('change');
                }
                if (data.entrega.personalizada != null) {
                    $('#ent_per_encargado').val(data.entrega.personalizada.encargado).trigger('change');
                    $('#ent_per_cedula').val(data.entrega.personalizada.cedula).trigger('change');
                    $('#ent_per_celular').val(data.entrega.personalizada.celular).trigger('change');
                    $('#ent_per_direccion').val(data.entrega.personalizada.direccion).trigger('change');
                    $('#ent_per_indicaciones').val(data.entrega.personalizada.indicaciones).trigger('change');
                    $('#ent_per_municipio').val(data.entrega.personalizada.municipio).trigger('change');
                    $('#ent_per_lugar').val(data.entrega.personalizada.lugar).trigger('change');
                    $('#ent_per_barrio').val(data.entrega.personalizada.barrio).trigger('change');
                    $('#ent_per_repartidores').val(data.entrega.personalizada.repartidores).trigger('change');
                    $('#ent_per_cel_repartidor').val(data.entrega.personalizada.cel_repartidor).trigger('change');
                } else {
                    $('#ent_tra_encargado').val(data.entrega.transportadora.encargado).trigger('change');
                    $('#ent_tra_cedula').val(data.entrega.transportadora.cedula).trigger('change');
                    $('#ent_tra_municipio').val(data.entrega.transportadora.municipio).trigger('change');
                    $('#ent_tra_barrio').val(data.entrega.transportadora.barrio).trigger('change');
                    $('#ent_tra_direccion').val(data.entrega.transportadora.direccion).trigger('change');
                    $('#ent_tra_indicaciones').val(data.entrega.transportadora.indicaciones).trigger('change');
                    $('#ent_tra_telefono').val(data.entrega.transportadora.telefono).trigger('change');
                    $('#ent_tra_empresa').val(data.entrega.transportadora.empresa).trigger('change');
                    $('#ent_tra_emp_telefono').val(data.entrega.transportadora.emp_telefono).trigger('change');
                    $('#ent_tra_taquilla').val(data.entrega.transportadora.taquilla).trigger('change');
                    $('#ent_tra_emp_info').val(data.entrega.transportadora.emp_info).trigger('change');
                    $('#ent_tra_nombre').val(data.entrega.transportadora.nombre).trigger('change');
                    $('#ent_tra_celular').val(data.entrega.transportadora.celular).trigger('change');
                    if (data.entrega.transportadora.hora) {
                        $('#ent_tra_hora').val(data.entrega.transportadora.hora.replace(/:\d\d([ ap]|$)/, '$1')).trigger('change');
                    }
                    $('#ent_tra_enc_costos').val(data.entrega.transportadora.enc_costos).trigger('change');
                }

                //Orden de recogida
                if (data.recogida != null) {
                    $('#rec_fecha').val(data.recogida.fecha).trigger('change');
                    if (data.recogida.hora){
                        $('#rec_hora').val(data.recogida.hora.replace(/:\d\d([ ap]|$)/, '$1')).trigger('change');
                    }
                    $('#rec_tipo_orden').val(data.recogida.tipo_orden).trigger('change');
                    $('#rec_observaciones').val(data.recogida.observaciones).trigger('change');
                    if (data.recogida.personalizada != null) {
                        $('#rec_per_encargado').val(data.recogida.personalizada.encargado).trigger('change');
                        $('#rec_per_cedula').val(data.recogida.personalizada.cedula).trigger('change');
                        $('#rec_per_celular').val(data.recogida.personalizada.celular).trigger('change');
                        $('#rec_per_direccion').val(data.recogida.personalizada.direccion).trigger('change');
                        $('#rec_per_indicaciones').val(data.recogida.personalizada.indicaciones).trigger('change');
                        $('#rec_per_municipio').val(data.recogida.personalizada.municipio).trigger('change');
                        $('#rec_per_lugar').val(data.recogida.personalizada.lugar).trigger('change');
                        $('#rec_per_barrio').val(data.recogida.personalizada.barrio).trigger('change');
                        $('#rec_per_repartidores').val(data.recogida.personalizada.repartidores).trigger('change');
                        $('#rec_per_cel_repartidor').val(data.recogida.personalizada.cel_repartidor).trigger('change');
                    } else {
                        $('#rec_tra_encargado').val(data.recogida.transportadora.encargado).trigger('change');
                        $('#rec_tra_cedula').val(data.recogida.transportadora.cedula).trigger('change');
                        $('#rec_tra_municipio').val(data.recogida.transportadora.municipio).trigger('change');
                        $('#rec_tra_barrio').val(data.recogida.transportadora.barrio).trigger('change');
                        $('#rec_tra_direccion').val(data.recogida.transportadora.direccion).trigger('change');
                        $('#rec_tra_indicaciones').val(data.recogida.transportadora.indicaciones).trigger('change');
                        $('#rec_tra_telefono').val(data.recogida.transportadora.telefono).trigger('change');
                        $('#rec_tra_empresa').val(data.recogida.transportadora.empresa).trigger('change');
                        $('#rec_tra_emp_telefono').val(data.recogida.transportadora.emp_telefono).trigger('change');
                        $('#rec_tra_taquilla').val(data.recogida.transportadora.taquilla).trigger('change');
                        $('#rec_tra_emp_info').val(data.recogida.transportadora.emp_info).trigger('change');
                        $('#rec_tra_nombre').val(data.recogida.transportadora.nombre).trigger('change');
                        $('#rec_tra_celular').val(data.recogida.transportadora.celular).trigger('change');
                        if (data.recogida.transportadora.hora) {
                            $('#rec_tra_hora').val(data.recogida.transportadora.hora.replace(/:\d\d([ ap]|$)/, '$1')).trigger('change');
                        }
                        $('#rec_tra_enc_costos').val(data.entrega.transportadora.enc_costos).trigger('change');
                    }
                }
                $('#descargarPDF-despacho, #descargarPDF-entrega-recogida').prop('disabled', false);
            } else{
                /// En caso contrario, recalcular las horas dependiendo de las fechas
                $('#ent_fecha').trigger('change');
                $('#fecha_entrega_des').trigger('change');
                $('#descargarPDF-despacho, #descargarPDF-entrega-recogida').prop('disabled', true);
            }
        });
    });

    /// Mostrar temporada en el pedido
    $('#fecha_evento').change(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_temporada', {
            fecha: $(this).val()
        }, function(data) {
            if (data.temporada != ''){
                $('#temporada-pedido').text('_'+data.temporada).removeAttr('style');
            }
        });
    });


    /// Copiar tipo de entrega entre pedido y orden
    $('#tipo_entrega_ord').change(function() {
        if ($(this).val() != null && $(this).val() != '') {
            $('#ent_tipo_orden').val($(this).val()).trigger('change');
        }
    });

    $('#ent_tipo_orden').change(function(event, flag) {
        if ($(this).val() != null && $(this).val() != '' && $('#prestamo').val() == 5) {
            $('#tipo_entrega_ord').val($(this).val()).removeClass('empty');
        }
    });

    /// Copiar tipo de recogida entre pedido y orden
    $('#tipo_recogida_ord').change(function() {
        if ($(this).val() != null && $(this).val() != '') {
            $('#rec_tipo_orden').val($(this).val()).trigger('change');
        }
    });

    $('#rec_tipo_orden').change(function(event, flag) {
        if ($(this).val() != null && $(this).val() != '' && $('#prestamo').val() == 5) {
            $('#tipo_recogida_ord').val($(this).val()).removeClass('empty');
        }
    });

    /// Numero de repartidores automatico
    $('#ent_tipo_orden, #rec_tipo_orden').change(function() {
        var prefix = $(this).attr('id').slice(0, 3);
        var togas = $('#detalles-0-pedida').val();
        if (togas && togas != '') {
            var repartidores = Math.ceil(parseInt(togas)/30);
            $('#' + prefix + '_per_repartidores').val(repartidores).removeClass('empty');
        }
    });

    /// Descargar todos los pdfs de las ordenes por fecha
    $('#descargar_pdf_ordenes').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_descargar_pdf_ordenes', {
            fecha: $('#fecha_orden').val()
        }, function(data) {
            if (data.flag == true){
                window.open("uploads/ordenes_despacho.zip");
            } else{
                $('#modal_error_pedido .alert').text('Error al descargar las ordenes');
                $('#modal_error_pedido').modal();
            }
        });
    });

    $('#descargar_pdf_ent_rec').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_descargar_pdf_ordenes_ent_rec', {
            fecha: $('#fecha_orden_entrega').val()
        }, function(data) {
            if (data.flag == true){
                window.open("uploads/ordenes_entrega_recogida.zip");
            } else{
                $('#modal_error_pedido .alert').text('Error al descargar las ordenes');
                $('#modal_error_pedido').modal();
            }
        });
    });

    /// Descargar informe en excel de las ordenes de entrega y recogida por fecha
    $('#descargar_excel_ent_rec').click(function() {
        var fecha = $('#fecha_orden_entrega').val(); 
        window.open('exportar_excel_entrega_recogida?fecha=' + fecha);
    });

    ///Modal de confirmacion de valor unitario
    $('#valor_uni').change(function(event, flag) {
        if (typeof flag == 'undefined'){
            $.getJSON($SCRIPT_ROOT + '/_formatear_valor', {
              valor: $(this).val()
            }, function(data) {
                $('#valor_moneda').text(data.moneda);
                $('#valor_letra').text(data.letra);
                $('#modal_valor').modal();
            }); 
        }
    });

    $('#cancelar_val_uni').click(function() {
        $('#valor_uni').val('');
    });
});