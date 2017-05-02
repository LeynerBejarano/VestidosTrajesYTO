function autocompletar() {
    var data = cedulas.slice();
    for (var i = data.length - 1; i >= 0; i--) {
        data[i] = String(data[i]);
    }
    $("#identificacion_enc").autocomplete({
        source: data,
        change: function() {
            $("#identificacion_enc").trigger('change');
            if($.inArray(parseInt($(this).val()), cedulas) >= 0){
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
            } else{
                $("#tipo_enc").val("NUEVO").trigger('change');
            }    
        }
    });
}

$(document).ready(function() {

    var id = null;

    $('input[type="submit"][value="Crear pedido"]').click(function() {
        $('.loader').show();
    });

    $('select.other').each(function() {
        $('#otro_'.concat($(this).attr('id'))).hide();
    });

    $('select.other').change(function() {
       if ($(this).val() == -1){
            $('#otro_'.concat($(this).attr('id'))).val(null);   
            $('#otro_'.concat($(this).attr('id'))).show();
        } else{
            $('#otro_'.concat($(this).attr('id'))).val($(this).val());
            $('#otro_'.concat($(this).attr('id'))).hide();
        } 
    });

    ///Obtener dias del mes seleccionado
    $("#mes_enc").change(function(event, dia) {
        $.getJSON($SCRIPT_ROOT + '/_cargar_dias', {
                  mes: $(this).val()
                }, function(data) {
                    $('#dia_enc').empty();
                    $.each(data.choices, function(index, value){
                        $('#dia_enc').append('<option value="'+value[0]+'">'+value[1]+'</option>');
                    });
                    if (typeof dia != 'undefined') {
                        $('#dia_enc').val(dia).trigger('change');
                    }
                });
                return false; 
    });

    // Definir area metropolitana (AM) a partir del valor seleccionado en el municipio
//PARA EL ENCARGADO
    $('#municipio_enc').change(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_area', {
                  id: $(this).val()
                }, function(data) {
                    if(data.area == 1){
                        $('#area_enc').text('AM')
                    } else if(data.area == 0){
                        $('#area_enc').text('FAM')
                    }
                });
                return false; 
    });


    function cargar_cliente(data) {
        id = data.id;
        if (typeof data.cliente != 'undefined'){
          $("#identificacion_enc").val(data.cliente.identificacion);
          $("#nombre_enc").val(data.cliente.nombre);
          $("#apellido_enc").val(data.cliente.apellido);
          $("#celular_enc").val(data.cliente.celular);
          $("#telefono_enc").val(data.cliente.telefono);
          $("#extension_enc").val(data.cliente.extension);
          $("#barrio_enc").val(data.cliente.barrio);
          $("#email_enc").val(data.cliente.email);
          $("#direccion_enc").val(data.cliente.direccion);
          $("#cargo_enc").val(data.cliente.cargo).trigger('change');
          $("#municipio_enc").val(data.cliente.ciudad).trigger('change');
          if (data.cliente.nacido_mes != null) {
            $("#mes_enc").val(data.cliente.nacido_mes).trigger('change', [data.cliente.nacido_dia]);
          }
          $("#tipo_enc").val("ANTIGUO");
          $('input, select').each(function() {
            if ($(this).val() == '' || $(this).val() == null) {
              $(this).addClass('empty');
            } else {
              $(this).removeClass('empty');
            }
          });
        }
    }

    $('.siguiente').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_encargado', {
          mod: 1,
          id: id
        }, function(data) {
            cargar_cliente(data);
        });
        return false;     
    });

    $('.anterior').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_encargado', {
          mod: -1,
          id: id
        }, function(data) {
            cargar_cliente(data);
        });
        return false;     
    });

    $('input, select').each(function() {
        if ($(this).val() == '' || $(this).val() == null) {
            $(this).addClass('empty');
        }
    });

     $('input, select').change(function() {
         if ($(this).val() == '' || $(this).val() == null) {
            $(this).addClass('empty');
         } else{
            $(this).removeClass('empty');
         }
     });  
});