var precios = {};
var precio_clase = 0;
var precio_estola = 0;
var precio_entrega = 0;
var precio_am = 0;
var val_unitario;
var test;


$(document).ready(function(){
    $('form').on('submit', function(event){
         event.preventDefault();
        $.ajax({
            //data : $('form').serialize(),
            data : {
               txtNonmbreCliente: $('#txtNonmbreCliente').val(),
               txtCC_Nit :$('#txtCC_Nit').val(),
               txtDiaCumpleaños:$('#txtDiaCumpleaños').val(),
               txtMesCumpleaños:$('#txtMesCumpleaños').val(),
               txtTelefonoFijo:$('#txtTelefonoFijo').val(),
               txtExtension:$('#txtExtension').val(),
               txtCelular:$('#txtCelular').val(),
               txtEmail:$('#txtEmail').val(),
                txtDireccion:$('#txtDireccion').val(),
               txtMunicipio:$('#txtMunicipio').val(),
              txtBarrio:$('#txtBarrio').val()
              //txtReferenciaNombre:$('#AjReferenciaNombre').val(),
             //txtReferenciaCelular:$('#AjReferenciaCelular').val(),
              //txtReferenciaTElefono:$('#AjReferenciaTelefono').val()
            },
            type: 'POST',
            url:'/insertarCliente'
        })
       // .done(function(data){
         //   if(data.error){
           //     $('#errorAlert').text(data.error).show();
            // //   $('#succesAlert').hide();
            //}else {
              //  $('#succesAlert').text(data.nombre).show();
                //$('#errorAlert').hide();
          //  }
        });
       
    });



