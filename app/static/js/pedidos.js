var precios = {};
var precio_clase = 0;
var precio_estola = 0;
var precio_entrega = 0;
var precio_am = 0;
var valor1;
var valor2;
var valor3;
var valor4;
var val_unitario;
var test;
var cerrar=1;
var LAId="ee";

$(document).ready(function(){
  $.ajax({         
            type: 'POST',
            url:'/FacturaActual',
            success: function(data){
            $('#txtConsecutivoActual').val(data.uno);                  
  }});
  $.ajax({         
            type: 'POST',
            url:'/MostrarBotonCambiadorDePass',
            success: function(data){
              if(data.toString() =="mostrar"){
                $('#idButtonMeterPassWord').show();
              }else{
                $('#idButtonCambiarWord').show();
              }
                              
  }});


var año = (new Date().getFullYear()).toString()
var TempoAlta_InicioFecha = new Date(año,"09", "30");
var Tempoalta_FinFecha = new Date(año,"12","30");
var todayDate = new Date();

if (todayDate > TempoAlta_InicioFecha || Tempoalta_FinFecha > todayDate) {
  $('#txtEntregarB').show()
  $('#txtReclamarB').show()  
}
else{
  $('#txtEntregarA').show()
  $('#txtReclamarA').show()
};
/*
$("#txtfechaEvento").on("input",function(){  
       $.ajax({
        type:"post",
        url:"/QuitarHoraReservada",
        data:{
                txtfechaEvento: $('#txtfechaEvento').val(),
                txtfechaRecoger: $('#txtfechaRecoger').val(),
        },
        success: function(data){
          if(data.tempo_rada != ""){
            if(data.tempo_rada == "alta"){
           for(var i = 0; i < data.lista.length; i++){

              $('#txtHoraReclamarA option[value="'+data.lista[i]+'"]').prop("disabled", true);
              } 
              $('#txtHoraReclamarA').show()
              $('#txtHoraReclamarA').hide()
            }else{
              for(var i = 0; i < data.lista.length; i++){

              $('#txtHoraReclamarB option[value="'+data.lista[i]+'"]').prop("disabled", true);
              } 
              $('#txtHoraReclamarA').hide()
              $('#txtHoraReclamarA').show()
            }
          
        }
        else{
              if(data.tempo_evento == "alta"){
           for(var i = 0; i < data.lista.length; i++){

              $('#txtHoraReclamarA option[value="'+data.lista[i]+'"]').prop("disabled", true);
              } 
              $('#txtHoraReclamarA').show()
              $('#txtHoraReclamarA').hide()
            }else{
              for(var i = 0; i < data.lista.length; i++){

              $('#txtHoraReclamarB option[value="'+data.lista[i]+'"]').prop("disabled", true);
              } 
              $('#txtHoraReclamarA').hide()
              $('#txtHoraReclamarA').show()
            }

          }
        }
          
      }); 
       
});
*/
function QuitarHora(recibi){  
  var recibido = recibi
       $.ajax({
        type:"post",
        url:"/QuitarHoraReservada",
        data:{
                txtfechaRecoger: recibido
                        },
        success: function(data){
          if(data.tempo_rada != ""){
            if(data.tempo_rada == "alta"){
           for(var i = 0; i < data.lista.length; i++){

              $('#txtHoraReclamarA option[value="'+data.lista[i]+'"]').prop("disabled", true);
              } 
              $('#txtHoraReclamarA').show()
              $('#txtHoraReclamarA').hide()
            }else{
              for(var i = 0; i < data.lista.length; i++){

              $('#txtHoraReclamarB option[value="'+data.lista[i]+'"]').prop("disabled", true);
              } 
              $('#txtHoraReclamarA').hide()
              $('#txtHoraReclamarA').show()
            }
          
        }
        else{
              if(data.tempo_evento == "alta"){
           for(var i = 0; i < data.lista.length; i++){

              $('#txtHoraReclamarA option[value="'+data.lista[i]+'"]').prop("disabled", true);
              } 
              $('#txtHoraReclamarA').show()
              $('#txtHoraReclamarA').hide()
            }else{
              for(var i = 0; i < data.lista.length; i++){

              $('#txtHoraReclamarB option[value="'+data.lista[i]+'"]').prop("disabled", true);
              } 
              $('#txtHoraReclamarA').hide()
              $('#txtHoraReclamarA').show()
            }

          }
        }
          
      }); 
       
}
$("#txtMunicipio").on("change",function(){  
  if($("#txtMunicipio").val().toString() =="-1"){
    Ingresar_Otros("Indique que ciudad",300,300,"#idCiudadOtro","ciudad")
    $("#txtMunicipio").prop('disabled', true);
}});
$("#txtMedioConocio").on("change",function(){  
  if($("#txtMedioConocio").val().toString() =="-1"){
    Ingresar_Otros("Indique que Medio de Comunicacion",300,300,"#idMedio_comunicacionOtro","MedioComuni")
    $("#txtMedioConocio").prop('disabled', true);
}});
$("#txtTipoEvento").on("change",function(){  
  if($("#txtTipoEvento").val().toString() =="-1"){
    Ingresar_Otros("Indique que tipo de evento",300,300,"#idTipo_EventoOtro","TipoEvento")
    $("#txtTipoEvento").prop('disabled', true);
}});
$("#idReciboButton").on("click",function(){  
  $('#txtConsecutivoRecibo').val($('#txtConsecutivo').val())
  $('#txtTipoPedidoRecibo').val($('#txtTipoPedido').val())
    Recibo("Ingresar Recibo",400,250);
  });
$("#idInformeTallerButton").on("click",function(){
  IngesarFechasTaller("Ingresar Fechas",400,250);
  });
$("#idInformeDiarioButton").on("click",function(){
    $.ajax({
        type:"post",
        url:"/GenerarInformeDiarioVersionFoto",
        success: function(data){

        }
      });
});

$('#Retefuente_tiene').on("change",function() {
    var total = parseInt($('#txtTotal').val())
        if(this.checked) {
         $('#txtRetefuente').val(total * 0.04)  
        }else{
          $('#txtRetefuente').val("")
        }       
});
$('#idFacturaPorCedulaButton').on("click",function() {
      $.ajax({
        type:"post",
        url:"/FacturasDeCedula",
        data:{
                txtCC_Nit: $('#txtCC_Nit').val()
        },
        success: function(data){
          for(var i = 0; i < data.FacNumero.length; i++){
            //$('#idTablaFacturaCedula tr:last').after('<tr><td>+data.FacNumero[i]+</td><td>+data.Valor[i]+</td><td>+data.Fecha[i]+</td><td>+data.Saldo[i]+</td></tr>');
            $('#idTablaFacturaCedula tr:last').after('<tr class="LineasTabla"><td class="LineasTabla"><a href="#" Onclick="CargarFactura('+data.FacNumero[i].toString()+')">'+data.FacNumero[i].toString()+'</a></td><td class="LineasTabla">'+data.Valor[i].toString()+'</td><td class="LineasTabla">'+data.Fecha[i].toString()+'</td><td class="LineasTabla">'+data.Saldo[i].toString()+'</td></tr>');
          }
        }
      });
      MostrarPopUpFacturaCC("Lista de facturas",600,300);
  });
$('#idReciboPorFacturaButton').on("click",function() {
      $.ajax({
        type:"post",
        url:"/ReciboDeFactura",
        data:{
                txtConsecutivoActual: $('#txtConsecutivoActual').val()
        },
        success: function(data){
          for(var i = 0; i < data.RecNumero.length; i++){
            //$('#idTablaFacturaCedula tr:last').after('<tr><td>+data.FacNumero[i]+</td><td>+data.Valor[i]+</td><td>+data.Fecha[i]+</td><td>+data.Saldo[i]+</td></tr>');
            $('#idTablaReciboFactura tr:last').after('<tr class="LineasTabla"><td class="LineasTabla"><a href="#" >'+data.RecNumero[i].toString()+'</a></td><td class="LineasTabla">'+data.Valor[i].toString()+'</td><td class="LineasTabla">'+data.Fecha[i].toString()+'</td><td class="LineasTabla">'+data.Saldo[i].toString()+'</td><td><button type="button" Onclick="Descargar_recibo('+data.RecNumero[i].toString()+')">Descargar</button></td></tr>');
          }
        }
      });
      MostrarPopUpRecibosFac("Lista de recibos",600,300);
  });
$('#idFacturaButton').click(function(){
   $.ajax({
        type:"post",
        url:"/GenerarFactura",
        data:{
                txtConsecutivoActual :$('#txtConsecutivoActual').val(),
                txtRetefuente: $('#txtRetefuente').val()
        }
      })
  }); 

$("#idLetraButton").on("click",function(){ 
      $.ajax({
        type:"post",
        url:"/GenerarLetra",
        data:{
                txtConsecutivoActual :$('#txtConsecutivoActual').val()
        }

      });
}); 
$('#txtfechaEvento').on('change', function(event){
  $.ajax({
        type:"post",
        url:"/PonerDiaDosDiasAparte",
        data:{
                txtfechaEvento :$('#txtfechaEvento').val()
        },
        success: function(data){
          $('#txtfechaRecoger').val(data.DosDiasAtrasString)
          $('#txtfechaDevolver').val(data.DosDiasDespuesString)
          $('#txtfechaRecogerVisible').val(data.DosDiasAtrasString)
          $('#txtfechaDevolverVisible').val(data.DosDiasDespuesString)
          QuitarHora(data.DosDiasAtrasString)
        }
      })
}); 
$('#txtfechaRecoger').on('input', function(event){
  $('#txtfechaRecogerVisible').val($('#txtfechaRecoger').val())
}); 
$('#txtfechaDevolver').on('input', function(event){
  $('#txtfechaDevolverVisible').val($('#txtfechaDevolver').val())
}); 

if($('#FechaDePedido').val()=="" ){
    $('#DivPriFechaFactura').show()
}
else{
    $('#DivPriFechaFactura').hide()
}

$('#txtMunicipio').on('change', function(event){

if ( ($('#txtDiaRecoger').val() != '') && ($('#txtMesRecoger').val() != '') && ($('#txtAñoRecoger').val() != '') && ($('#txtDiaEntregar').val() != '') && ($('#txtMesEntregar').val() != '') && ($('#txtAñoEntregar').val() != '') ){

    $.ajax({
            
            data:{
                txtCC_Nit :$('#txtCC_Nit').val(),
                txtfac_prenda1: $('#txtfac_prenda1').val(),
                txtfac_prenda2: $('#txtfac_prenda2').val(),
                txtfac_prenda3: $('#txtfac_prenda3').val(),
                txtfac_prenda4: $('#txtfac_prenda4').val(),
                txtAñoRecoger:$('#txtAñoRecoger').val(),
                txtDiaRecoger:$('#txtDiaRecoger').val(),
                txttMesRecoger:$('#txtMesRecoger').val(),
                txtDiaEntregar:$('#txtDiaEntregar').val(),
                txtMesEntregar:$('#txtMesEntregar').val(),
                txtAñoEntregar:$('#txtAñoEntregar').val()
            },
            type: 'POST',
            url:'/UsuarioNuevoViejo',
            success: function(data){
            $('#NuevoViejo').text(data.antiguedad)
            $('#NuevoViejo').show()
            if(data.antiguedad.toString() =="viejo"){
              $('#txtNonmbreCliente').val(data.nombre)
              $('#txtMunicipio').val(data.ciudad)
              $('#txtDireccion').val(data.direccion)
              $('#txtEmail').val(data.email)
              $('#txtCelular').val(data.celular)
              $('#txtTelefonoFijo').val(data.telefono)
              $('#txtExtension').val(data.extension)
              $('#txtTelefonoFijoOficina').val(data.telefonoFijo)
              $('#ExtOficina').val(data.telefonoFijo_ext)
              $('#txtBarrio').val(data.barrio)
              $('#txtMedioConocio').val(data.medioConocio)
              $('#txtDiaCumpleaños').val(data.nacido_dia)
              $('#txtMesCumpleaños').val(data.nacido_mes)
              
            }
                        
  }
        })
}

}) 
$("#idTotalButton").on('click', function(event){
  var  txtValoresReferenciaArray = []
           for(var i = 1; i < 22 ; i++){
            if($('#ReferenciaPrenda'+i.toString()).val()!=""){
            txtValoresReferenciaArray.push($('#txtValorReferencia'+i.toString()).val())
            }
              }
     $.ajax({   
            data:{
                txtValoresReferenciaArray :txtValoresReferenciaArray
            },
            type: 'POST',
            url:'/ValorTotalEnLetras',
            success: function(data){
            $('#txtTotal').val(data.numeros)
            $('#idTotalenTexto').val(data.letras)
                        
  }
        }) 
})
  /*  
if( ($('#txtDiaRecoger').val() != '') && ($('#txtMesRecoger').val() != '') && ($('#txtAñoRecoger').val() != '') && ($('#txtDiaEntregar').val() != '') && ($('#txtMesEntregar').val() != '') && ($('#txtAñoEntregar').val() != '')  ) {
  $.ajax({
            
            data:{
                txtDiaRecoger : $('#txtDiaRecoger').val(),
                txtMesRecoger: $('#txtMesRecoger').val(),
                txtAñoRecoger: $('#txtAñoRecoger').val(),
                txtDiaEntregar : $('#txtDiaEntregar').val(),
                txtMesEntregar : $('#txtMesEntregar').val(),
                txtAñoEntregar : $('#txtAñoEntregar').val(),
                txtPrenda: $('#txtPrenda').val()
            },
            
            //data : $('form').serialize(),
            type: 'POST',
            url:'/UsuarioNuevoViejo',
          success: function(data){
            $('#NuevoViejo').text(data)
            $('#NuevoViejo').show()
                        
  }
            //success: function(data) {
              //         window.location = Json.parse(data); 
                // }

        })  

} */

$("#txtfechaEvento").on('input', function(event){
      $.ajax({
            
            data:{
                txtCC_Nit :$('#txtCC_Nit').val()
            },
            
            //data : $('form').serialize(),
            type: 'POST',
            url:'/UsuarioNuevoViejo',
          success: function(data){
            $('#NuevoViejo').text(data)
            $('#NuevoViejo').show()
                        
  }

        })

})
$('#txtCC_Nit').on('input', function(event){
    $.ajax({
            data:{
              txtCC_Nit :$('#txtCC_Nit').val()
            },
            //data : $('form').serialize(),
            type: 'POST',
            url:'/UsuarioNuevoViejo',
          success: function(data){
            $('#NuevoViejo').text(data.antiguedad)
            $('#NuevoViejo').show()
            $('#txtNonmbreCliente').val(data.nombre)
            $('#txtDiaCumpleaños').val(data.nacido_dia)
            $('#txtMesCumpleaños').val(data.nacido_mes)
            $('#txtTelefonoFijo').val(data.telefono)
            $('#txtExtension').val(data.extension)
            $('#txtTelefonoFijoOficina').val(data.telefonoFijo)
            $('#ExtOficina').val(data.telefonoFijo_ext)
            $('#txtCelular').val(data.celular)
            $('#txtDireccion').val(data.direccion)
            $('#txtBarrio').val(data.barrio)
            $('#txtMunicipio').val(data.ciudad)
            $('#txtEmail').val(data.email)
            $('#txtMedioConocio').val(data.medioConocio)
                        
  }

        })

        $.ajax({
            
            data:{
                txtCC_Nit :$('#txtCC_Nit').val()

            },
            
            //data : $('form').serialize(),
            type: 'POST',
            url:'/BuscarNumeroDeFacturas',
          success: function(data){
            $('#txtTotalFacturaCliente').val(data)
                        
  }

        })


})
$('#txtFacturaActual_Relacivo').on('input', function(event){
  $.ajax({
            
            data:{
                txtFacturaActual_Relacivo :$('#txtFacturaActual_Relacivo').val(),
                txtCC_Nit :$('#txtCC_Nit').val()

            },
            
            //data : $('form').serialize(),
            type: 'POST',
            url:'/BuscarFacturaRelativo',
          success: function(data){
            $('#txtConsecutivo').val(data)
                        
  }

        })
})

$('#SiguienteFactura').click(function(){

        $.ajax({
            
            data:{
                txtCC_Nit :$('#txtCC_Nit').val(),
                txtConsecutivo: $('#txtConsecutivo').val()

            },
            //data : $('form').serialize(),
            type: 'POST',
            url:'/siguienteFactura',
            
             success: function(data){
                        $('#txtConsecutivo').val(data.fac_numero)
                        $('#txtConsecutivoManual').val(data.fac_consecutivoManual)
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
                        $('#txtfechaEvento').val(data.fac_eventoFecha)
                        $('#txtDiaEvento').val(data.fac_eventoDia)
                        $('#txtMesEvento').val(data.fac_eventoMes)
                        $('#txtAñoEvento').val(data.fac_eventoAño)
                        $('#ReferenciaPrenda1').val(data.fac_ReferenciaProducto1)
                        $('#ReferenciaPrenda2').val(data.fac_ReferenciaProducto2)
                        $('#ReferenciaPrenda3').val(data.fac_ReferenciaProducto3)
                        $('#ReferenciaPrenda4').val(data.fac_ReferenciaProducto4)
                        $('#txtDescripcion1').val(data.fac_descripcion1)
                        $('#txtDescripcion2').val(data.fac_descripcion2)
                        $('#txtDescripcion3').val(data.fac_descripcion3)
                        $('#txtDescripcion4').val(data.fac_descripcion4)
                        $('#txtAccesorios1').val(data.fac_accesorios1)
                        $('#txtAccesorios2').val(data.fac_accesorios2)
                        $('#txtAccesorios3').val(data.fac_accesorios3)
                        $('#txtAccesorios4').val(data.fac_accesorios4)
                        $('#txtMedidasArreglos1').val(data.fac_MedidasArreglos1)
                        $('#txtMedidasArreglos2').val(data.fac_MedidasArreglos2)
                        $('#txtMedidasArreglos3').val(data.fac_MedidasArreglos3)
                        $('#txtMedidasArreglos4').val(data.fac_MedidasArreglos4)
                        $('#txtValorReferencia1').val(data.fac_ValorReferencia1)
                        $('#txtValorReferencia2').val(data.fac_ValorReferencia2)
                        $('#txtValorReferencia3').val(data.fac_ValorReferencia3)
                        $('#txtValorReferencia4').val(data.fac_ValorReferencia4)
                        $('#txtValorSugerencia1').val(data.fac_ValorReferencia1)
                        $('#txtValorSugerencia2').val(data.fac_ValorReferencia2)
                        $('#txtValorSugerencia3').val(data.fac_ValorReferencia3)
                        $('#txtValorSugerencia4').val(data.fac_ValorReferencia4)
                        $('#txtDiaRecoger').val(data.fac_ReclamarMercanciaDia)
                        $('#txtMesRecoger').val(data.fac_ReclamarMercanciaMes)
                        $('#txtAñoRecoger').val(data.fac_ReclamarMercanciaAño)
                        $('#txtDiaEntregar').val(data.fac_DevolverMercanciaDia)
                        $('#txtMesEntregar').val(data.fac_DevolverMercanciaMes)
                        $('#txtAñoEntregar').val(data.fac_DevolverMercanciaAño)
                        $('#txtTotal').val(data.fac_Total)
                        $('#txtTotalVisible').val(data.fac_Total)
                        $('#txtAbono').val(data.fac_Abono)
                        $('#txtSaldo').val(data.fac_Saldo)
                        $('#txtRetefuente').val(data.fac_Retefuente)
                        $('#txtfechaRecoger').val(data.fechaInicio)
                        $('#txtfechaDevolver').val(data.fechaFinal)
                        $('#txtNota').val(data.fac_nota)
                        $('#FechaDePedido').val(data.ac_fechaFactura) 
                        $('#txtConsecutivoActual').val(data.fac_numero)
                        $('#cantidadRealPrenda1').val(data.fac_CantidadLLeva1)
                        $('#cantidadRealPrenda2').val(data.fac_CantidadLLeva2)
                        $('#cantidadRealPrenda3').val(data.fac_CantidadLLeva3)
                        $('#cantidadRealPrenda4').val(data.fac_CantidadLLeva4)
                        $('#idTablaReciboFactura  td').remove();
                        CargarTablaRecibos(data.fac_numero)
                    for(var i = 1; i <= data.ReferenciaLista.length; i++){
                    $('#RowPrenda'+i.toString()).show()
                    $('#ReferenciaPrenda'+i.toString()).val(data.ReferenciaLista[i-1])
                    $('#txtDescripcion'+i.toString()).val(data.DescripcionLista[i-1])
                    $('#txtAccesorios'+i.toString()).val(data.AccesoriosLista[i-1])    
                    $('#txtValorReferencia'+i.toString()).val(data.ValorREferencia[i-1])
                    $('#LineaSexo'+i.toString()).val(data.LineaSExo[i-1])
                    $('#Estilo'+i.toString()).val(data.EstilosLista[i-1])
                    $('#txtMedidasArreglos'+i.toString()).val(data.MedidasYarreglos[i-1])
                     }
                     for(var i = 21; i >= data.ReferenciaLista.length; i--){
                      if($('#ReferenciaPrenda'+i.toString()).val() == ""){
                         $('#RowPrenda'+i.toString()).hide()
                      }
                     
                     }
                     if($('#ReferenciaPrenda1').val() == ""){
                      $('#RowPrenda1').show()
                     }
                     if(data.invalidar == "si"){
                      $("#detalles :input").prop("disabled", true);
                      $("#txtTotal").prop('disabled', true);
                     }
                         
  }
            //success: function(data) {
              //         window.location = Json.parse(data); 
                // }

        })
         
    })

$('#SiguienteFactura').click(function(){

        $.ajax({
            
            data:{
                txtCC_Nit :$('#txtCC_Nit').val(),
                txtConsecutivo: $('#txtConsecutivo').val()

            },
            //data : $('form').serialize(),
            type: 'POST',
            url:'/CuantosRecibos',
             success: function(data){
                        $('#txtTotalDeRecibos_Relacivo').val(data) 

  }
            //success: function(data) {
              //         window.location = Json.parse(data); 
                // }


        })
         
    })

$('#MostrarRecibo').click(function(){

        $.ajax({
            
            data:{
                txtReciboActual_Relacivo :$('#txtReciboActual_Relacivo').val(),
                txtConsecutivo: $('#txtConsecutivo').val()

            },
            //data : $('form').serialize(),
            type: 'POST',
            url:'/MostrarRecibo',
             success: function(data){
                        $('#txtReciFacturaNumeroMostrar').val(data.reci_Factura)
                        $('#txtReciNumeroMostrar').val(data.reci_numero)
                        $('#txtReciValorMostrar').val(data.reci_valor)
                        $('#txtReciCiudadMostrar').val(data.Ciudad_Fecha)
                        $('#txtReciRecibimosDeMostrar').val(data.RecibimosDe)
                        $('#txtReciSumaEnLetrasMostrar').val(data.reci_AporteEnLetras)
                        $('#txtReciPorconceptodeMostrar').val(data.reci_Concepto)
                        $('#txtReciSuNuevoSaldoEsMostrar').val(data.reci_nuevoSaldo)
                        $('#txtTipoPedido').val(data.reci_FacturaTipo)
                        MostrarRecibo("Recibo para mostrar",400,400);
  }
            //success: function(data) {
              //         window.location = Json.parse(data); 
                // }


        })
         
    })

$('#GuardarRecibo').click(function(){

        $.ajax({
            
            data:{
                txtConsecutivo :$('#txtConsecutivo').val(),
                txtReciValor: $('#txtReciValor').val(),
                txtReciCiudad: $('#txtMunicipio').val(),
                txtReciRecibimosDe: $('#txtReciRecibimosDe').val(),
                txtReciSuSaldoEnLetras: $('#txtReciSuSaldoEnLetras').val(),
                txtReciPorconceptode: $('#txtReciPorconceptode').val(),
                txtTotal: $('#txtTotal').val(),
                txtTipoPedido: $('#txtTipoPedido').val(),
                txtReciSuNuevoSaldoEs: $('#txtReciSuNuevoSaldoEs').val(),
                txtCC_Nit: $('#txtReciSuNuevoSaldoEs').val()
            },
            //data : $('form').serialize(),
            type: 'POST',
            url:'/siguienteFactura',
            
             success: function(data){
                                              
  }
            //success: function(data) {
              //         window.location = Json.parse(data); 
                // }


        })
         
    })
  $('#txtReciValor').on('keyup', function(event){
    $.ajax({
            
            data:{
                txtConsecutivo :$('#txtConsecutivo').val(),
                txtReciValor: $('#txtReciValor').val()
            },
            //data : $('form').serialize(),
            type: 'POST',
            url:'/NuevoSaldo',
            
             success: function(data){
              $('#txtReciSuNuevoSaldoEs').val(data)                                
  }
            //success: function(data) {
              //         window.location = Json.parse(data); 
                // }


        })
         
    })

  $('#txtReciValor').on('keyup', function(event){

        $.ajax({
            
            data:{
                txtConsecutivo :$('#txtConsecutivo').val(),
                txtReciValor: $('#txtReciValor').val()
            },
            //data : $('form').serialize(),
            type: 'POST',
            url:'/ReciboPorConceptoDe',
            
             success: function(data){
              $('#txtReciPorconceptode').val(data)                                 
  }
            //success: function(data) {
              //         window.location = Json.parse(data); 
                // }


        })
        $.ajax({
            
            data:{
                txtReciValor: $('#txtReciValor').val()
            },
            //data : $('form').serialize(),
            type: 'POST',
            url:'/NumeroEnLetras',
            
             success: function(data){
              $('#txtReciSuSaldoEnLetras').val(data)                                 
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
               //txtTelefonoFijo:$('#txtTelefonoFijo').val(data.cli_telefono),
               //txtExtension:$('#txtExtension').val(data.cli_extension),           
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

     
       
   


    $('#idButtonGrabar').on('click', function(event){
      if($('#txtMunicipio').is(':disabled')){
        var muni =  $('#CiudadOtro').val()
      }else{
        var muni = $('#txtMunicipio').val()
      }
      if($('#txtMedioConocio').is(':disabled')){
        var medium =  $('#Medio_comunicacionOtro').val()
      }else{
        var medium = $('#txtMedioConocio').val()
      }
      if($('#txtTipoEvento').is(':disabled')){
        var type =  $('#Tipo_EventoOtro').val()
      }else{
        var type = $('#txtTipoEvento').val()
      }
         event.preventDefault();
         var  ReferenciaPrendaArray  = []
         var  txtDescripcionArray = []
         var  txtAccesoriosArray = []
         var  txtMedidasArreglosArray = []
         var  EstiloArray = []
         var  LineaSexoArray = []
         var  txtValorReferenciaArray = []
         for(var i = 1; i < 22 ; i++){
            if($('#ReferenciaPrenda'+i.toString()).val()!=""){
            ReferenciaPrendaArray.push($('#ReferenciaPrenda'+i.toString()).val())
            txtDescripcionArray.push($('#txtDescripcion'+i.toString()).val())
            txtAccesoriosArray.push($('#txtAccesorios'+i.toString()).val())
            txtMedidasArreglosArray.push($('#txtMedidasArreglos'+i.toString()).val())
            EstiloArray.push($('#Estilo'+i.toString()).val())
            LineaSexoArray.push($('#LineaSexo'+i.toString()).val())
            txtValorReferenciaArray.push($('#txtValorReferencia'+i.toString()).val())
            }
              }
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
               txtTelefonoFijoOficina:$('#txtTelefonoFijoOficina').val(),
               ExtOficina:$('#ExtOficina').val(),
               txtCelular:$('#txtCelular').val(),
               txtEmail:$('#txtEmail').val(),
               txtDireccion:$('#txtDireccion').val(),

               txtMunicipio:$('#txtMunicipio').val(),
               txtBarrio:$('#txtBarrio').val(),
               txtMunicipio:muni,
               txtMedioConocio:medium ,
              //txtAtendidoPor://$('#txtAtendidoPor').val(),
              txtReferenciaNombre:$('#txtReferenciaNombre').val(),
              txtReferenciaCelular:$('#txtReferenciaCelular').val(),
              txtReferenciaTelefono:$('#txtReferenciaTelefono').val(),
              txtTipoPedido:$('#txtTipoPedido').val(),
              txtTipoEvento:type,
              txtPedPoblacion:$('#txtPedPoblacion').val(),
              txtDiaEvento:$('#txtDiaEvento').val(),
              txtMesEvento:$('#txtMesEvento').val(),
              txtAñoEvento:$('#txtAñoEvento').val(),
              txtReferencia1:$('#ReferenciaPrenda1').val(),
              txtDescripcion1:$('#txtDescripcion1').val(),
              txtAccesorios1:$('#txtAccesorios1').val(),
              txtMedidasArreglos1:$('#txtMedidasArreglos1').val(),
              txtValorReferencia1:$('#txtValorReferencia1').val(),
              txtReferencia2:$('#ReferenciaPrenda2').val(),
              txtDescripcion2:$('#txtDescripcion2').val(),
              txtAccesorios2:$('#txtAccesorios2').val(),
              txtMedidasArreglos2:$('#txtMedidasArreglos2').val(),
              txtValorReferencia2:$('#txtValorReferencia2').val(),
              txtReferencia3:$('#ReferenciaPrenda3').val(),
              txtDescripcion3:$('#txtDescripcion3').val(),
              txtAccesorios3:$('#txtAccesorios3').val(),
              txtMedidasArreglos3:$('#txtMedidasArreglos3').val(),
              txtValorReferencia3:$('#txtValorReferencia3').val(),
              txtReferencia4:$('#ReferenciaPrenda4').val(),
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
              txtNota:$('#txtNota').val(),
              txtHoraReclamarA:$('#txtHoraReclamarA').val(),
              txtHoraReclamarB:$('#txtHoraReclamarB').val(),
              txtHoraDevolverB:$('#txtHoraDevolverB').val(),
              txtHoraDevolverA:$('#txtHoraDevolverA').val(),
              txtfechaEvento: $('#txtfechaEvento').val(),
              txtRetefuente:$('#txtRetefuente').val(),
              txtfechaEvento:$('#txtfechaEvento').val(),
              txtfechaRecoger:$('#txtfechaRecoger').val(),
              txtfechaDevolver:$('#txtfechaDevolver').val(),
              txtHoraDevolverB:$('#txtHoraDevolverB').val(),
              txtHoraReclamarB:$('#txtHoraReclamarB').val(),
              txtHoraDevolverA:$('#txtHoraDevolverA').val(),
              txtHoraReclamarA:$('#txtHoraReclamarA').val(),
              cantidadRealPrenda1:$('#cantidadRealPrenda1').val(),
              cantidadRealPrenda2:$('#cantidadRealPrenda2').val(),
              cantidadRealPrenda3:$('#cantidadRealPrenda3').val(),
              cantidadRealPrenda4:$('#cantidadRealPrenda4').val(),
              txtConsecutivoActual:$('#txtConsecutivoActual').val(),
              ReferenciaPrendaArray:ReferenciaPrendaArray,
              txtDescripcionArray:txtDescripcionArray,
              txtAccesoriosArray:txtAccesoriosArray,
              txtMedidasArreglosArray:txtMedidasArreglosArray,
              EstiloArray:EstiloArray,
              LineaSexoArray:LineaSexoArray,
              txtValorReferenciaArray:txtValorReferenciaArray   
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



$("#Retefuente_tiene, #txtTotal").change(function() {
    if($("#Retefuente_tiene").attr('checked')) {
        if($('#txtTotal').val() ==("") ){
          $('#txtRetefuente').val("")
        }
        else{
          $('#txtRetefuente').val(parseInt($('#txtTotal').val())*0.1)
        }
    }
    else{
      $('#txtRetefuente').val("")
    }
});



$('#txtTotal').on('change paste keyup', function(event){
  alert("cambio")
});



function Recibo(titulo,ancho,alto){
  $("#idRecibo").dialog({
    title:titulo,
      width:ancho,
      height:alto,
      modal:true,
      buttons:{
      Ingresar:Ingresar_recibo,
      Cancelar:function(){
        $(this).dialog('close');
      }
    }   
  });
}

function Ingresar_recibo(){  

    $.ajax({
        type:"post",
        url:"/GuardarRecibo",
        data:{
                txtConsecutivo :$('#txtConsecutivo').val(),
                txtReciValor: $('#txtReciValor').val(),
                txtMunicipio: $('#txtMunicipio').val(),
                txtReciRecibimosDe: $('#txtReciRecibimosDe').val(),
                txtReciSumaEnLetras: $('#txtReciSumaEnLetras').val(),
                txtReciPorconceptode: $('#txtReciPorconceptode').val(),
                txtTotal: $('#txtTotal').val(),
                txtTipoPedido: $('#txtTipoPedido').val(),
                txtReciSuNuevoSaldoEs: $('#txtReciSuNuevoSaldoEs').val(),
                txtCC_Nit: $('#txtReciSuNuevoSaldoEs').val(),
                txtReciSuSaldoEnLetras: $('#txtReciSuSaldoEnLetras').val(),
                txtCC_Nit: $('#txtCC_Nit').val()
        },
        success:function(resultado){
          alert(resultado);
         
        }
      });
    
  
}
function Descargar_recibo(reciboNum){  
 var reciboNumero = reciboNum;
 var ConsecutivoN = $('#txtConsecutivoActual').val();
    $.ajax({
        type:"post",
        url:"/descargar_recibo",
        data:{
                ConsecutivoN :ConsecutivoN,
                reciboNumero: reciboNumero,
                txtCC_Nit: $('#txtCC_Nit').val()
        }
      });
    
  
}

function MostrarRecibo(titulo,ancho,alto){
  $("#idMostrarRecibo").dialog({
    title:titulo,
      width:ancho,
      height:alto,
      modal:true,
      buttons:{
      Descargar:Descargar_recibo,
      Cancelar:function(){
        $(this).dialog('close');
      }
    }

    }) 
  };
  function IngesarFechasTaller(titulo,ancho,alto){
  $("#idInformeTaller").dialog({
    title:titulo,
      width:ancho,
      height:alto,
      modal:true,
      buttons:{
      Generar :GenerarInformeTaller,
      Cancelar:function(){
        $(this).dialog('close');
      }
    }   
  });
}
function GenerarInformeTaller(){  

    $.ajax({
        type:"post",
        url:"/GenerarInformeTaller",
        data:{
                txtFechaTallerInicio :$('#txtFechaTallerInicio').val(),
                txtFechaTallerFinal: $('#txtFechaTallerFinal').val()
        }
      });
    
  
}

function MostrarPopUpFacturaCC(titulo,ancho,alto){
  $("#idPopUpFacturasCedula").dialog({
    title:titulo,
      width:ancho,
      height:alto,
      modal:true,
      buttons:{
      "Close":function cerrar(){
        $('#idTablaFacturaCedula  td').remove();
        $(this).dialog('close')
      },
      Cancelar:function(){
        $('#idTablaFacturaCedula  td').remove();
        $(this).dialog('close')
      }
    }
  });
}
  function MostrarPopUpRecibosFac(titulo,ancho,alto){
  $("#idListaRecibo").dialog({
    title:titulo,
      width:ancho,
      height:alto,
      modal:true,
      buttons:{
      "Close":function cerrar(){
        $('#idTablaReciboFactura  td').remove();
        $(this).dialog('close')
      },
      Cancelar:function(){
        $('#idTablaReciboFactura  td').remove();
        $(this).dialog('close')
      }
    }
  });
}
function CargarFactura(FacturaNumero){
$.ajax({
        type:"post",
        url:"/siguienteFactura",
        data:{
                txtCC_Nit :$('#txtCC_Nit').val(),
                txtConsecutivo: FacturaNumero
        },
        success: function(data){
                        $('#txtConsecutivo').val(data.fac_numero)
                        $('#txtConsecutivoManual').val(data.fac_consecutivoManual)
                        $('#tipoPedido').val(data.tipoPedido)
                        $('#txtReferenciaNombre').val(data.fac_ReferenciaNombre)
                        $('#txtReferenciaCelular').val(data.fac_ReferenciaCelular)
                        $('#txtPedPoblacion').val(data.fac_poblacion)
                        $('#txtConsecutivo').val(data.fac_numero)
                        $('#ConsecutivoManual').val(data.fac_consecutivoManual)
                        $('#txtNonmbreCliente').val(data.cli_nombre)
                        $('#txtCC_Nit').val(data.cli_identificacion)
                        $('#txtTelefonoFijo').val(data.cli_telefono)
                        $('#txtExtension').val(data.cli_extension)
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
                        $('#txtfechaEvento').val(data.fac_eventoFecha)
                        $('#txtDiaEvento').val(data.fac_eventoDia)
                        $('#txtMesEvento').val(data.fac_eventoMes)
                        $('#txtAñoEvento').val(data.fac_eventoAño)
                        $('#ReferenciaPrenda1').val(data.fac_ReferenciaProducto1)
                        $('#ReferenciaPrenda2').val(data.fac_ReferenciaProducto2)
                        $('#ReferenciaPrenda3').val(data.fac_ReferenciaProducto3)
                        $('#ReferenciaPrenda4').val(data.fac_ReferenciaProducto4)
                        $('#txtDescripcion1').val(data.fac_descripcion1)
                        $('#txtDescripcion2').val(data.fac_descripcion2)
                        $('#txtDescripcion3').val(data.fac_descripcion3)
                        $('#txtDescripcion4').val(data.fac_descripcion4)
                        $('#txtAccesorios1').val(data.fac_accesorios1)
                        $('#txtAccesorios2').val(data.fac_accesorios2)
                        $('#txtAccesorios3').val(data.fac_accesorios3)
                        $('#txtAccesorios4').val(data.fac_accesorios4)
                        $('#txtMedidasArreglos1').val(data.fac_MedidasArreglos1)
                        $('#txtMedidasArreglos2').val(data.fac_MedidasArreglos2)
                        $('#txtMedidasArreglos3').val(data.fac_MedidasArreglos3)
                        $('#txtMedidasArreglos4').val(data.fac_MedidasArreglos4)
                        $('#txtValorReferencia1').val(data.fac_ValorReferencia1)
                        $('#txtValorReferencia2').val(data.fac_ValorReferencia2)
                        $('#txtValorReferencia3').val(data.fac_ValorReferencia3)
                        $('#txtValorReferencia4').val(data.fac_ValorReferencia4)
                        $('#txtValorSugerencia1').val(data.fac_ValorReferencia1)
                        $('#txtValorSugerencia2').val(data.fac_ValorReferencia2)
                        $('#txtValorSugerencia3').val(data.fac_ValorReferencia3)
                        $('#txtValorSugerencia4').val(data.fac_ValorReferencia4)
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
                        $('#txtfechaRecoger').val(data.fac_ReclamarMercanciaFecha)
                        $('#txtfechaDevolver').val(data.fac_DevolverMercanciaFecha)
                        $('#txtNota').val(data.fac_nota)
                        $('#FechaDePedido').val(data.ac_fechaFactura) 
                        $('#txtConsecutivoActual').val(data.fac_numero)
                        $('#cantidadRealPrenda1').val(data.fac_CantidadLLeva1)
                        $('#cantidadRealPrenda2').val(data.fac_CantidadLLeva2)
                        $('#cantidadRealPrenda3').val(data.fac_CantidadLLeva3)
                        $('#cantidadRealPrenda4').val(data.fac_CantidadLLeva4)
                        $('#txtDiaCumpleaños').val(data.cli_nacido_dia)
                        $('#txtMesCumpleaños').val(data.cli_nacido_mes)
                        for(var i = 1; i < data.ReferenciaLista.length; i++){
                    $('#ReferenciaPrenda'+i.toString()).val(data.ReferenciaLista[i])
                    $('#txtDescripcion'+i.toString()).val(data.DescripcionLista[i])
                    $('#txtAccesorios'+i.toString()).val(data.AccesoriosLista[i])    
                    $('#txtValorReferencia'+i.toString()).val(data.ValorREferencia[i])
                    $('#LineaSexo'+i.toString()).val(data.LineaSExo)
                    $('#Estilo'+i.toString()).val(data.EstilosLista[i])
                    $('#txtMedidasArreglos'+i.toString()).val(data.MedidasYarreglos[i])
              $('#idTablaFacturaCedula tr:last').after('<tr class="LineasTabla"><td class="LineasTabla"><a href="#" Onclick="CargarFactura('+data.FacNumero[i].toString()+')">'+data.FacNumero[i].toString()+'</a></td><td class="LineasTabla">'+data.Valor[i].toString()+'</td><td class="LineasTabla">'+data.Fecha[i].toString()+'</td><td class="LineasTabla">'+data.Saldo[i].toString()+'</td></tr>');
          }


        }
      });
  $(this).dialog('close');
}
function CambiarPassword(){
  CambiusContraseñus("cambiar contraseña",300,300)
}
function CargarTablaRecibos(datad){

  $.ajax({
        type:"post",
        url:"/ReciboDeFactura",
        data:{txtConsecutivoActual: datad},
        success: function(data){
          for(var i = 0; i < data.RecNumero.length; i++){
            //$('#idTablaFacturaCedula tr:last').after('<tr><td>+data.FacNumero[i]+</td><td>+data.Valor[i]+</td><td>+data.Fecha[i]+</td><td>+data.Saldo[i]+</td></tr>');
            $('#idTablaReciboFactura tr:last').after('<tr class="LineasTabla"><td class="LineasTabla"><a href="#" >'+data.RecNumero[i].toString()+'</a></td><td class="LineasTabla">'+data.Valor[i].toString()+'</td><td class="LineasTabla">'+data.Fecha[i].toString()+'</td><td class="LineasTabla">'+data.Saldo[i].toString()+'</td><td><button type="button" Onclick="Descargar_recibo('+data.RecNumero[i].toString()+')">Descargar</button></td></tr>');
          }}});}
function IngresarMedidas(titulo,ancho,alto,selector,input){
  $(selector).dialog({
    title:titulo,
      width:ancho,
      height:alto,
      modal:true,
      buttons:{
      Ingresar:function PonerMedidasInput(input){
       $.ajax({
        type:"post",
        url:"/PonerMedidaYArreglo",
        data:{
                InputMeter:$('#InputMeter').val(),
                LMLargoManga :$('#LMLargoManga').val(),
                LMCintura: $('#LMCintura').val(),
                LMLargoPantalon: $('#LMLargoPantalon').val(),
                HombreArreglo: $('#HombreArreglo').val(),
                LFBusto: $('#LFBusto').val(),
                LFCintura: $('#LFCintura').val(),
                LFCadera: $('#LFCadera').val(),
                LFLargoTotal: $('#LFLargoTotal').val(),
                MujerArreglo: $('#MujerArreglo').val()
        },
        success: function(data){
          $('#'+data.input).val(data.datus)
          $('#LMLargoManga').val("")
          $('#LMCintura').val("")
          $('#LMLargoPantalon').val("")
          $('#LFBusto').val("")
          $('#LFCintura').val("")
          $('#LFCadera').val("")
          $('#LFLargoTotal').val("")
          $('#MujerArreglo').val("")
          $('#HombreArreglo').val("")
        }
      });
       cerrar = 0

       $(this).dialog('close');
      },
      Cancelar:function(){ 
      cerrar = 0
        $(this).dialog('close');

      }
    }   
  });
}
function CambiusContraseñus(titulo,ancho,alto){
    $("#SectionPasswordOwner").dialog({
      title:titulo,
      width:ancho,
      height:alto,
      modal:true,
      buttons:{
      Ingresar:function ChangePW(input){
        $.ajax({
        type:"post",
        url:"/VendedorIngresandoPassWord",
        data:{
                PasswordSkillOwner:$('#PasswordSkillOwner').val()

        },
        success: function(data){
          alert(data)
        }
 
      });
}}})}
function CuadritoMeterContraseña(titulo,ancho,alto){
    $("#SectionPassword").dialog({
      title:titulo,
      width:ancho,
      height:alto,
      modal:true,
      buttons:{
      Ingresar:function PassPutter(input){
        $.ajax({
        type:"post",
        url:"/CambiarContraseñaDeSistema",
        data:{
                txtPassEnviado:$('#txtPassEnviado').val()
        },
        success: function(data){
          if(data.toString() =="siEra"){
            alert("contraseña correcta")
            $('#PasswordSAVED').val(data)
          }else{
            alert("contraseña incorrecta")
          }}});}}})}
function Ingresar_Otros(titulo,ancho,alto,selectorOtro,opcion){
  var opcionOtru = opcion
    $(selectorOtro).dialog({
      title:titulo,
      width:ancho,
      height:alto,
      modal:true,
      buttons:{
      Ingresar:function PonerElOtro(input){
        $.ajax({
        type:"post",
        url:"/PonerOtros",
        data:{
                CiudadOtro:$('#CiudadOtro').val(),
                Medio_comunicacionOtro :$('#Medio_comunicacionOtro').val(),
                Tipo_EventoOtro: $('#Tipo_EventoOtro').val(),
                opcionOtru: opcionOtru
        }
      });
        $(this).dialog('close');
}}})}
function alerta(x){
    if($('#'+x.toString()).val()==""){
    $('#InputMeter').val(x)
    var number;
    var temp = x.toString().slice((x.length)-1,(x.length));
    if($.isNumeric(temp)){
      number = x.toString().slice((x.length)-1,(x.length));
    }
    else
    {
      number = x.toString().slice((x.length)-2,(x.length))
    }
    
    if (cerrar==0){
         $(':focus').blur()
          cerrar = 1
          //$("#"+x).val(LaId)
    }
    else{
          if($('#LineaSexo'+number).val() =="LineaMasculina") {
          IngresarMedidas("Medidas Linea Masculina",300,300,"#idMedidasLineaMasculina",x.toString())
        }
        else{
          var selector = "#idMedidasLineaFemenina"
           IngresarMedidas("Medidas Linea Femenina",300,300,"#idMedidasLineaFemenina",x.toString())
        }
    } 
    }

};
function AutomatizarCortesia(x){
  //$(this).prop('checked', true);
  
    $('#InputMeter').val(x)
    var number;
    var temp = x.toString().slice((x.length)-1,(x.length));
    if($.isNumeric(temp)){
      number = x.toString().slice((x.length)-1,(x.length));
    }
    else
    {
      number = x.toString().slice((x.length)-2,(x.length))
    } 
    var novias = 0
    var corNum = 0
    var RegaloJohn = 0
    if($("#"+x.toString()).is(':checked')){
        $.ajax({    
      data:{
        ReferenciaPrenda: $('#ReferenciaPrenda'+number).val(),
        PasswordSAVED: $('#PasswordSAVED').val()
    },
    type: 'POST',
    url:'/AlterarPrecioTreinta',          
     success: function(data){
      $('#txtValorReferencia'+number).val(data.precio)                                  
  }})
    }else{
    if($("#PasswordSAVED").val().toString() == "siEra"){
          $("#txtValorReferencia"+number.toString()).val("0")
        }
    else{
         for(var i = 1; i <= 21; i++){
          if($("#txtDescripcion"+i.toString()).val() == "novia"){
            novias = novias + 1;
          }}
        for(var i = 1; i <= 21; i++){
         if($("#Cortesia"+i.toString()).is(':checked')){ 
          corNum = corNum + 1;
        } }
        if((novias*3) <= corNum){
          $('#'+x.toString()).prop('checked', false);
          alert("entro a la parte que lo deja uncheck")
        } 
        else{
          $("#txtValorReferencia"+number.toString()).val('0')
        }}}}
function MostrarOcultarTrBelow(w){
    var number;
    var MasUno;
    var temp = w.toString().slice((w.length)-2,(w.length));
    if($.isNumeric(temp)){
      number = w.toString().slice((w.length)-2,(w.length));
      MasUno = parseInt(w+1).toString().slice((w.length)-2,(w.length));
    }
    else
    {
      number = w.toString().slice((w.length)-1,(w.length))
      MasUno = parseInt(w+1).toString().slice((w.length)-1,(w.length))
    }
    if($('#RowPrenda'+number).css('display') == 'none'){
      $('#RowPrenda'+number).show()
      $("#idRowPrendaButton"+w).hide()
      $("#idRowOcultarButton"+w).hide()
    }
    else{
      $('#RowPrenda'+number).hide()
    }
 } 
 function AlterarPrecio(w){
    var number;
    var temp = w.toString().slice((w.length)-2,(w.length));
    if($.isNumeric(temp)){
      number = w.toString().slice((w.length)-2,(w.length));

    }
    else
    {
      number = w.toString().slice((w.length)-1,(w.length))
    }
  $.ajax({    
    data:{
        ReferenciaPrenda: $('#ReferenciaPrenda'+number).val(),
        txtValorReferencia: $('#txtValorReferencia'+number).val(),
        input:w,
        PasswordSAVED: $('#PasswordSAVED').val()
    },
    type: 'POST',
    url:'/AlterarPrecioTreinta',          
     success: function(data){
      $('#txtValorReferencia'+number).val(data.precio)
      if(data.respuesta.toString() != "cambio permitido"){
        alert(data.respuesta)  
      }                                     
  }
})
 }
  function VerificarFecha(x){
    var fecha = $('#'+x.toString()).val().toString()
    var DiasFestivo = ["20/07/2017","2017-07-20", "07/08/2017","2017-08-07", "21/08/2017","2017-08-21", "16/10/2017","2017-10-16","06/11/2017","2017-11-06","13/11/2017","2017-11-13","08/12/2017","2017-12-08","25/12/2017","2017-12-25"];
    for(var i = 0; i < DiasFestivo.length; i++){
      if(fecha == DiasFestivo[i]){
        alert("es festivo, ingrese otra fecha")
        $('#'+x.toString()).val("")
      }
    }
}
 function ObtenerTotal(){
  var total = 0
  for(var i = 1; i <= 21; i++){
    if($("#txtValorReferencia"+i.toString()).val() != ""){
      total = total + parseInt($("#txtValorReferencia"+i.toString()).val())
    }
  } 
  $("#txtTotal").val(total.toString())
 }
function MeterPassword(){
  CuadritoMeterContraseña("Ingrese contraseña",300,300)
}
/*
function AlterarFechasParaReserva(){
    $.ajax({    
    data:{
        txtReferencia: $('#ReferenciaPrenda'+number).val(),
        txtfechaRecoger:$('#txtfechaRecoger').val(),
        txtfechaDevolver:$('#txtfechaDevolver').val()
    },
    type: 'POST',
    url:'/AutomatizarPrenda',          
     success: function(data){
      $('#txtDescripcion'+number).val(data.descripcion)
      $('#txtAccesorios'+number).val(data.accesorios) 
      $('#txtValorReferencia'+number).val(data.valor_sugerido) 
      $('#LineaSexo'+number).val(data.sexo)   
      //alert(data.fecha_prueba1)
      //alert(data.fecha_prueba2)   
      if(data.reservaResulT != "no"){
        $('#EstaReservado_'+number).text(data.reservaResulT)  
         $('#EstaReservado_'+number).show()
      }
      else{
        $('#EstaReservado_'+number).text("")  
         $('#EstaReservado_'+number).hide()
      }                      
  }
})
}
*/
function AutomatizarConRefyReser(w){
    var number;
    var temp = w.toString().slice((w.length)-2,(w.length));
    if($.isNumeric(temp)){
      number = w.toString().slice((w.length)-2,(w.length));

    }
    else
    {
      number = w.toString().slice((w.length)-1,(w.length))
    }
    $.ajax({    
    data:{
        txtReferencia: $('#ReferenciaPrenda'+number).val(),
        txtfechaRecoger:$('#txtfechaRecoger').val(),
        txtfechaDevolver:$('#txtfechaDevolver').val()
    },
    type: 'POST',
    url:'/AutomatizarPrenda',          
     success: function(data){
      $('#txtDescripcion'+number).val(data.descripcion)
      $('#txtAccesorios'+number).val(data.accesorios) 
      $('#txtValorReferencia'+number).val(data.valor_sugerido) 
      $('#LineaSexo'+number).val(data.sexo)   
      //alert(data.fecha_prueba1)
      //alert(data.fecha_prueba2)   
      if(data.reservaResulT != "no"){
        $('#EstaReservado_'+number).text(data.reservaResulT)  
         $('#EstaReservado_'+number).show()
      }
      else{
        $('#EstaReservado_'+number).text("")  
         $('#EstaReservado_'+number).hide()
      }                      
  }
})

}

function ValorTotalEnLetras(){
      $.ajax({    
    data:{
        txtTotal: $('#txtTotal').val()
    },
    type: 'POST',
    url:'/ValorTotalEnLetras',          
     success: function(data){
      $('#txtTotalLetras').val(data)               
  }
})
}
function RealOcultar(w){
    var number;
    var temp = w.toString().slice((w.length)-2,(w.length));
    if($.isNumeric(temp)){
      number = w.toString().slice((w.length)-2,(w.length));

    }
    else
    {
      number = w.toString().slice((w.length)-1,(w.length))
    }
    $('#ReferenciaPrenda'+number).hide()
    $('#idRowPrendaButton'+number).hide() 
}

function AdherirFila(){
var i= 1;
var j=2;
  while(i<22){
    if($('#RowPrenda'+i.toString()).css('display') != 'none' && $('#RowPrenda'+j.toString()).css('display') == 'none'){
      i =22;
      $('#RowPrenda'+j.toString()).show()
  }else{
    i=i+1;
    j=j+1;
  }
}
}
function DisminuirFilaFila(){

 i= 1;
 j=2;

  while(i<22){
    if($('#RowPrenda'+i.toString()).css('display') != 'none' && $('#RowPrenda'+j.toString()).css('display') != 'none'){
      i =22;
      $('#RowPrenda'+j.toString()).hide()
      $('#ReferenciaPrenda'+j.toString()).val("")
      $('#txtDescripcion'+j.toString()).val("")
      $('#txtAccesorios'+j.toString()).val("")
      $('#txtMedidasArreglos'+j.toString()).val("")
      $('#Estilo'+j.toString()).val("")
      $('#LineaSexo'+j.toString()).val("")
      $('#txtValorReferencia'+j.toString()).val("")
  }else{
    i=i+1;
    j=j+1;
  }
}
}
/////////////////////////////////////////////////////////////////////////////////////////////////7
//////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////7
/////////////////////////////////////////////////////////////////////////////////////////////////7
//////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////7
/////////////////////////////////////////////////////////////////////////////////////////////////7
//////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////7







