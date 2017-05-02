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
                    if ($('#clase').val() == 3) {
                       $("#color").append('<option value="-1">Otro</option>'); 
                    }
                    $.each(data.estilos, function(index, value){
                        $("#estilo").append('<option value="'+value[0]+'">'+value[1]+'</option>');
                    });
                    if (typeof color != 'undefined'){
                        $('#color').val(color);
                    }
                    if (typeof estilo != 'undefined'){
                        $('#estilo').val(estilo);
                    }
                    $('#color').trigger('change');
                    $('#estilo').trigger('change');

                });
                return false; 
    });

    function cargar_accesorio(data) {
        id = data.id;
        if (typeof data.accesorio != 'undefined'){
            $('#linea').val(data.accesorio.linea).trigger('change', [data.accesorio.clase, data.accesorio.color, data.accesorio.estilo]);
            $('#nombre').val(data.accesorio.nombre).trigger('change');
            $('#cantidad').val(data.accesorio.cantidad).trigger('change');
            $('#val_unitario').val(data.accesorio.val_unitario).trigger('change');
        }
    }

    $('.siguiente').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_accesorio', {
          mod: 1,
          id: id
        }, function(data) {
            cargar_accesorio(data);
        });
        return false;     
    });

    $('.anterior').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_cargar_accesorio', {
          mod: -1,
          id: id
        }, function(data) {
            cargar_accesorio(data);
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


    $('#color').change(function() {
       if ($(this).val() == -1){
            $('#otro_color').val(null);   
            $('#otro_color').show();
        } else{
            $('#otro_color').val($(this).val());
            $('#otro_color').hide();
        } 
    });

    $('#color').trigger('change');


    /////Mostrar/Ocultar datos de la estola
    if ($('#clase').val() == 4) {
        $('div.estola').show();
    } else{
        $('div.estola').hide();
    }

    $('#clase').change(function() {
        if ($(this).val() == 4) {
            $('div.estola').show();
        } else{
            $('div.estola').hide();
        }
    });

});