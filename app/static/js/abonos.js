$(document).ready(function() {
    $('input[type="submit"][value="Grabar"]').click(function() {
        $('.loader').show();
    });
    $('select').append('<option selected disabled>-</option>');

    $('#exportar_abonos').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_exportar_abonos', {
          id: $('#pedido').val()
        }, function(data) {
            if (data.flag == true) {
                window.open('uploads/informe_abonos.pdf');
            } else{
                $('#modal_error .alert').text('Error: no existe el pedido ingresado');
                $('#modal_error').modal();
            }
        });   
    });

    $('#grabar').click(function() {
        $.getJSON($SCRIPT_ROOT + '/_formatear_valor', {
          valor: $('#valor').val()
        }, function(data) {
            $('#valor_moneda').text(data.moneda);
            $('#valor_letra').text(data.letra);
            $('#modal_valor').modal();
        }); 
    });

    $('#confirmar').click(function() {
        $('form').submit();
    });
});