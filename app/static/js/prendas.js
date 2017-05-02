$(document).ready(function() {
    var id = null;

    $('#linea').change(function(event, clase, color, estilo) {
        $.getJSON($SCRIPT_ROOT + '/_cargar_clases', {
                  id: $(this).val(),
                  tipo: tipo
                }, function(data) {
                    $('#clase').attr('disabled', false);
                    $('#clase').empty();
                    $.each(data.clases, function(index, value){
                        $("#clase").append('<option value="'+value[0]+'">'+value[1]+'</option>');
                    });
                    if (typeof clase != 'undefined'){
                        $('#clase').val(clase);
                    }
                    $('#clase').trigger('change', [color, estilo]);
                });
                return false; 
    });

    $('#clase').change(function(event, color, estilo) {
        $.getJSON($SCRIPT_ROOT + '/_cargar_colores_estilos', {
                  id: $(this).val()
                }, function(data) {
                    $('#color').attr('disabled', false);
                    $('#estilo').attr('disabled', false);
                    $('#color').empty();
                    $('#estilo').empty();
                    $.each(data.colores, function(index, value){
                        $("#color").append('<option value="'+value[0]+'">'+value[1]+'</option>');
                    });
                    $.each(data.estilos, function(index, value){
                        $("#estilo").append('<option value="'+value[0]+'">'+value[1]+'</option>');
                    });
                    if (typeof color != 'undefined'){
                        $('#color').val(color);
                    }
                    if (typeof estilo != 'undefined'){
                        $('#estilo').val(estilo);
                    }
                    $('#estilo').trigger('change');
                    $('#color').trigger('change');
                });
                return false; 
    });

    function cargar_prenda(data) {
        id = data.id;
        if (typeof data.prenda != 'undefined'){
            $('#linea').val(data.prenda.linea).trigger('change', [data.prenda.clase, data.prenda.color, data.prenda.estilo]);
            $('#nombre').val(data.prenda.nombre).trigger('change');
            $('#cantidad').val(data.prenda.cantidad).trigger('change');
            $('#piezas').val(data.prenda.piezas).trigger('change');
            $('#filename').val(data.prenda.imagen);
            $('#val_unitario').val(data.prenda.val_unitario).trigger('change');
        }
    }

    $('.siguiente').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_prenda', {
          mod: 1,
          id: id
        }, function(data) {
            cargar_prenda(data);
        });
        return false;     
    });

    $('.anterior').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_prenda', {
          mod: -1,
          id: id
        }, function(data) {
            cargar_prenda(data);
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

     /////Mostrar nombre de la imagen seleccionada
     $('#imagen').change(function() {
        if ($('#imagen')[0].files[0]) {
            $('#filename').text($('#imagen')[0].files[0].name);
        } else{
            $('#filename').text('Ningún archivo seleccionado');
        }
     });

     $('#imagen').trigger('change');
});