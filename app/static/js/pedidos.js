var precios = {};
var precio_clase = 0;
var precio_estola = 0;
var precio_entrega = 0;
var precio_am = 0;
var val_unitario;
var test;


$(document).ready(function(){
    $('form').on('submit', function(event){
        
        $.ajax({
            data : {
               txtNonmbreCliente: $('#AjNombre').val(),
               txtCC_Nit :$('#AjCcNit').val(),
               txtDiaCumpleaños:$('#AjDiaCumpleaños').val(),
               txtMesCumpleaños:$('#AjMesCumpleaños').val(),
               txtTelefonoFijo:$('#AjTelefonoFijo').val(),
               Ext:$('#AjExt').val(),
               txtCelular:$('#AjCelular').val(),
               txtEmail:$('#AjEmail').val(),
               txtDireccion:$('#AjDireccion').val(),
               txtMunicipio:$('#AjMunicipio').val(),
               txtBarrio:$('#AjBarrio').val(),
               txtReferenciaNombre:$('#AjReferenciaNombre').val(),
               txtReferenciaCelular:$('#AjReferenciaCelular').val(),
               txtReferenciaTElefono:$('#AjReferenciaTelefono').val()
            },
            type: 'POST',
            url:'/insertarCliente'
        })
        .done(function(data){
            if(data.error){
                $('#errorAlert').text(data.error).show();
                $('#succesAlert').hide();
            }else {
                $('#succesAlert').text(data.nombre).show();
                $('#errorAlert').hide();
            }
        });
        event.preventDefault();
    })
});


