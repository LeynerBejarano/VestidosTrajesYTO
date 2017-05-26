var precios = {};
var precio_clase = 0;
var precio_estola = 0;
var precio_entrega = 0;
var precio_am = 0;
var val_unitario;
var test;


$(document).ready(function(){



$('#SiguienteFactura').click(function(){

        $.ajax({
            
            data:{
                txtConsecutivo: $('#txtConsecutivo').val()

            },
            //data : $('form').serialize(),
            type: 'POST',
            url:'/siguienteFactura',
            
             success: function(data){
                        $('#tipoPedido').val(data.tipoPedido)
                        $('#txtReferenciaNombre').val(data.fac_ReferenciaNombre)
                        $('#txtReferenciaCelular').val(data.fac_ReferenciaCelular)
                        $('#txtPedPoblacion').val(data.fac_poblacion)

                        $('#txtConsecutivo').val(data.fac_numero)
                        $('#ConsecutivoManual').val(data.fac_consecutivoManual)
                        $('#txtNonmbreCliente').val(data.cli_nombre)
                        $('#txtCC_Nit').val(data.cli_identificacion)
                        $('#txtDiaCumpleaños').val(data.cli_nacido_dia)
                        $('#txtMesCumpleaños').val(data.cli_nacido_mes)
                        $('#txtTelefonoFijo').val(data.cli_telefono)
                        $('#txtExtension').val(data.cli_extension)
                        $('#txtCelular').val(data.cli_celular)
                        $('#txtEmail').val(data.cli_email)
                        $('#txtDireccion').val(data.cli_direccion)   
                        $('#txtMunicipio').val(data.cli_ciudad)
                        $('#txtMedioConocio').val(data.cli_medioConocio)
                        $('#txtBarrio').val(data.cli_barrio)
                        $('#txtAtendidoPor').val(data.fac_AtendidoPor)
                        $('#txtReferenciaNombre').val(data.fac_ReferenciaNombre)
                        $('#txtReferenciaCelular').val(data.fac_ReferenciaCelular)
                        $('#txtReferenciaTelefono').val(data.fac_ReferenciaMedio)
                        $('#txtTipoPedido').val(data.fac_tipoPedido)
                        $('#txtPedPoblacion').val(data.fac_poblacion)
                        $('#txtTipoEvento').val(data.fac_evento)
                        $('#txtDiaEvento').val(data.fac_eventoDia)
                        $('#txtMesEvento').val(data.fac_eventoMes)
                        $('#txtAñoEvento').val(data.fac_eventoAño)
                        $('#txtReferencia1').val(data.fac_ReferenciaProducto1)
                        $('#txtReferencia2').val(data.fac_ReferenciaProducto2)
                        $('#txtReferencia3').val(data.fac_ReferenciaProducto3)
                        $('#txtReferencia4').val(data.fac_ReferenciaProducto4)
                        $('#txtDescripcion1').val(data.fac_descripcion1)
                        $('#txtDescripcion2').val(data.fac_descripcion2)
                        $('#txtDescripcion3').val(data.fac_descripcion3)
                        $('#txtDescripcion4').val(data.fac_descripcion4)
                        $('txtAccesorios1').val(data.fac_accesorios1)
                        $('txtAccesorios2').val(data.fac_accesorios2)
                        $('txtAccesorios3').val(data.fac_accesorios3)
                        $('txtAccesorios4').val(data.fac_accesorios4)
                        $('#txtMedidasArreglos1').val(data.fac_MedidasArreglos1)
                        $('#txtMedidasArreglos2').val(data.fac_MedidasArreglos2)
                        $('#txtMedidasArreglos3').val(data.fac_MedidasArreglos3)
                        $('#txtMedidasArreglos4').val(data.fac_MedidasArreglos4)
                        $('#txtValorReferencia1').val(data.fac_ValorReferencia1)
                        $('#txtValorReferencia2').val(data.fac_ValorReferencia2)
                        $('#txtValorReferencia3').val(data.fac_ValorReferencia3)
                        $('#txtValorReferencia4').val(data.fac_ValorReferencia4)
                        $('#txtDiaRecoger').val(data.fac_ReclamarMercanciaDia)
                        $('#txtMesRecoger').val(data.fac_ReclamarMercanciaMes)
                        $('#txtAñoRecoger').val(data.fac_ReclamarMercanciaAño)
                        $('#txtDiaEntregar').val(data.fac_DevolverMercanciaDia)
                        $('#txtMesEntregar').val(data.fac_DevolverMercanciaMes)
                        $('#txtAñoEntregar').val(data.fac_DevolverMercanciaAño)
                        $('#txtTotal').val(data.fac_Total)
                        $('#txtAbono').val(data.fac_Abono)
                        $('#txtSaldo').val(data.fac_Saldo)
                        $('#txtRetefuente').val(data.fac_Retefuente)
                        $('#txtNota').val(data.fac_nota)
                         
  }
            //success: function(data) {
              //         window.location = Json.parse(data); 
                // }


        })
         
    })

$('#Descargar').click(function(){

        $.ajax({
            
            data:{
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
               txtBarrio:$('#txtBarrio').val(),
               txtMunicipio:$('#txtMunicipio').val(),
               txtMedioConocio:$('#txtMedioConocio').val(),
               txtAtendidoPor:$('#txtAtendidoPor').val(),
              txtConsecutivo:$('#txtConsecutivo').val(),
              txtConsecutivoManual:$('#txtConsecutivoManual').val(),
              txtReferenciaNombre:$('#txtReferenciaNombre').val(),
              txtReferenciaCelular:$('#txtReferenciaCelular').val(),
              txtReferenciaTelefono:$('#txtReferenciaTelefono').val(),
              txtTipoPedido:$('#txtTipoPedido').val(),
              txtTipoEvento:$('#txtTipoEvento').val(),
              txtPedPoblacion:$('#txtPedPoblacion').val(),
              txtDiaEvento:$('#txtDiaEvento').val(),
              txtMesEvento:$('#txtMesEvento').val(),
              txtAñoEvento:$('#txtAñoEvento').val(),
              txtReferencia4:$('#txtReferencia1').val(),
              txtDescripcion4:$('#txtDescripcion1').val(),
              txtAccesorios4:$('#txtAccesorios1').val(),
              txtMedidasArreglos4:$('#txtMedidasArreglos1').val(),
              txtValorReferencia4:$('#txtValorReferencia1').val(),
              txtReferencia4:$('#txtReferencia2').val(),
              txtDescripcion4:$('#txtDescripcion2').val(),
              txtAccesorios4:$('#txtAccesorios2').val(),
              txtMedidasArreglos4:$('#txtMedidasArreglos2').val(),
              txtValorReferencia4:$('#txtValorReferencia2').val(),
              txtReferencia4:$('#txtReferencia3').val(),
              txtDescripcion4:$('#txtDescripcion3').val(),
              txtAccesorios4:$('#txtAccesorios3').val(),
              txtMedidasArreglos4:$('#txtMedidasArreglos3').val(),
              txtValorReferencia4:$('#txtValorReferencia3').val(),
              txtReferencia4:$('#txtReferencia4').val(),
              txtDescripcion4:$('#txtDescripcion4').val(),
              txtAccesorios4:$('#txtAccesorios4').val(),
              txtMedidasArreglos4:$('#txtMedidasArreglos4').val(),
              txtValorReferencia4:$('#txtValorReferencia4').val(),
              txtAñoRecoger:$('#txtAñoRecoger').val(),
              txtDiaRecoger:$('#txtDiaRecoger').val(),
              txttMesRecoger:$('#txtMesRecoger').val(),
              txtDiaEntregar:$('#txtDiaEntregar').val(),
              txtMesEntregar:$('#txtMesEntregar').val(),
              txtAñoEntregar:$('#txtAñoEntregar').val(),
              txtTotal:$('#txtTotal').val(),
              txtAbono:$('#txtAbono').val(),
              txtSaldo:$('#txtSaldo').val(),
              txtRetefuente:$('#txtRetefuente').val(),
              txtNota:$('#txtNota').val()
            },
            
            //data : $('form').serialize(),
            type: 'POST',
            url:'/_descargar_pdf'
          /*   success: function(data){
                        var file_path = data;
                        var a = document.createElement('A');
                        a.href = file_path;
                        a.download = file_path.substr(file_path.lastIndexOf('/') + 1);
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
  }*/
            //success: function(data) {
              //         window.location = Json.parse(data); 
                // }

        })
         
    })

     
       
   


    $('form').on('submit', function(event){
         event.preventDefault();
        $.ajax({
            //data : $('form').serialize(),
            data : {

               txtConsecutivoManual: $('#txtConsecutivoManual').val(),
               txtConsecutivo: $('#txtConsecutivo').val(),
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
               txtBarrio:$('#txtBarrio').val(),
               txtMunicipio:$('#txtMunicipio').val(),
               txtMedioConocio:$('#txtMedioConocio').val(),
              //txtAtendidoPor://$('#txtAtendidoPor').val(),
              txtReferenciaNombre:$('#txtReferenciaNombre').val(),
              txtReferenciaCelular:$('#txtReferenciaCelular').val(),
              txtReferenciaTelefono:$('#txtReferenciaTelefono').val(),
              txtTipoPedido:$('#txtTipoPedido').val(),
              txtTipoEvento:$('#txtTipoEvento').val(),
              txtPedPoblacion:$('#txtPedPoblacion').val(),
              txtDiaEvento:$('#txtDiaEvento').val(),
              txtMesEvento:$('#txtMesEvento').val(),
              txtAñoEvento:$('#txtAñoEvento').val(),
              txtReferencia4:$('#txtReferencia1').val(),
              txtDescripcion4:$('#txtDescripcion1').val(),
              txtAccesorios4:$('#txtAccesorios1').val(),
              txtMedidasArreglos4:$('#txtMedidasArreglos1').val(),
              txtValorReferencia4:$('#txtValorReferencia1').val(),
              txtReferencia4:$('#txtReferencia2').val(),
              txtDescripcion4:$('#txtDescripcion2').val(),
              txtAccesorios4:$('#txtAccesorios2').val(),
              txtMedidasArreglos4:$('#txtMedidasArreglos2').val(),
              txtValorReferencia4:$('#txtValorReferencia2').val(),
              txtReferencia4:$('#txtReferencia3').val(),
              txtDescripcion4:$('#txtDescripcion3').val(),
              txtAccesorios4:$('#txtAccesorios3').val(),
              txtMedidasArreglos4:$('#txtMedidasArreglos3').val(),
              txtValorReferencia4:$('#txtValorReferencia3').val(),
              txtReferencia4:$('#txtReferencia4').val(),
              txtDescripcion4:$('#txtDescripcion4').val(),
              txtAccesorios4:$('#txtAccesorios4').val(),
              txtMedidasArreglos4:$('#txtMedidasArreglos4').val(),
              txtValorReferencia4:$('#txtValorReferencia4').val(),
              txtDiaRecoger:$('#txtDiaRecoger').val(),
              txtDiaRecoger:$('#txtMesRecoger').val(),
              txtDiaEntregar:$('#txtAñoEntregar').val(),
              txtMesEntregar:$('#txtMesEntregar').val(),
              txtAñoEntregar:$('#txtAñoEntregar').val(),
              txtTotal:$('#txtTotal').val(),
              txtAbono:$('#txtAbono').val(),
              txtSaldo:$('#txtSaldo').val(),
              txtRetefuente:$('#txtRetefuente').val(),
              txtNota:$('#txtNota').val()
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
    
     
       
    







