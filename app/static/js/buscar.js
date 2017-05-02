
$(document).ready(function() {
    
    $('#lista-pedidos').hide();
    $('input[type="submit"]').hide();
    
    $(window).bind('beforeunload',function(){
        $('.loader').show();
    });

    $('select').append('<option selected disabled>-</option>')

    $('#buscar').click(function() {
        $('.loader').show();
        $.getJSON($SCRIPT_ROOT + '/_buscar_pedidos', {
          consecutivo: $("#consecutivo").val(),
          identificacion: $("#identificacion").val(),
          cli_nombre: $("#cli_nombre").val(),
          cli_apellido: $("#cli_apellido").val(),
          cli_ciudad: $("#cli_ciudad").val(),
          nit: $("#nit").val(),
          ins_nombre: $("#ins_nombre").val(),
          ins_ciudad: $("#ins_ciudad").val()
        }, function(data) {
          $('#lista-pedidos tbody').empty();
          if (data.pedidos.length != 0){
            $('#lista-pedidos').show();
            $('input[type="submit"]').show();
            for (var i = 0; i < data.pedidos.length; i++) {
                data.pedidos[i];
                $('#lista-pedidos tbody').append(
                  '<tr id="pedido-'+ data.pedidos[i].pedido.numero +'"> \
                    <td>\
                    <input type="radio" name="pedido" id="'+ data.pedidos[i].pedido.numero +'"> \
                    ' + data.pedidos[i].pedido.numero + '\
                    </td>\
                    <td>'+ data.pedidos[i].pedido.fecha + '</td> \
                    <td>'+ data.pedidos[i].cliente.identificacion +'</td> \
                    <td>' + data.pedidos[i].cliente.nombre + '</td> \
                    <td>' + data.pedidos[i].cliente.apellido + '</td> \
                    <td>' + data.pedidos[i].cliente.ciudad + '</td>\
                    <td>' + data.pedidos[i].cliente.email + '</td>\
                    <td>' + data.pedidos[i].institucion.nit + '</td>\
                    <td colspan="2">' + data.pedidos[i].institucion.nombre + '</td>\
                    <td>' + data.pedidos[i].institucion.ciudad + '</td>\
                    <td>' + data.pedidos[i].det_pedido.jornada + '</td>\
                    <td>' + data.pedidos[i].det_pedido.poblacion + '</td>\
                  </tr>')

                   $('input[name="pedido"]').click(function() {
                        if ($(this).is(':checked')) {
                            $('tr.selected').removeClass('selected');
                            $('#pedido-' + $(this).attr('id')).addClass('selected');
                            $('#pedido').val($(this).attr('id'));
                        }
                    });
            }
          } else {
            $('#lista-pedidos').hide();
            $('input[type="submit"]').hide();
          }
          $('.loader').hide();
        }); 
        return false;
    });

});

