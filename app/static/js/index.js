$('.error-page').hide(0);
$('.login-button').click(function() {
  $('.loader').show();
});

$('.login-button , .no-access').click(function(){
  $('.login').slideUp(500);
  $('.error-page').slideDown(1000);
});

$('.try-again').click(function(){
  $('.error-page').hide(0);
  $('.login').slideDown(1000);
});

$(function(){
  $('.hide-show').show();
  $('.hide-show span').addClass('show')
  
  $('.hide-show span').click(function(){
    if( $(this).hasClass('show') ) {
      $(this).text('Hide');
      $('input[name="clave"]').attr('type','text');
      $(this).removeClass('show');
    } else {
       $(this).text('Show');
       $('input[name="clave"]').attr('type','password');
       $(this).addClass('show');
    }
  });
	
	$('form button[type="submit"]').on('click', function(){
		$('.hide-show span').text('Show').addClass('show');
		$('.hide-show').parent().find('input[name="clave"]').attr('type','password');
	}); 
});