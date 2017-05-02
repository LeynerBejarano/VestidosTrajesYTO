$(document).ready(function(){
	$('a[href="pedidos"],a[href="buscar"]').click(function() {
		$('.loader').show();
	});
	$('#modal_messages').modal();

	$("#portfolio-contant-active").mixItUp();


	$("#testimonial-slider").owlCarousel({
	    paginationSpeed : 500,      
	    singleItem:true,
	    autoPlay: 3000,
	});

    // $(document).ajaxStart($.blockUI).ajaxStop($.unblockUI);

    $(document).ajaxStart(function(){
        $('.loader').show();
        $.blockUI({ message: '' }); 
    });
    $(document).ajaxStop(function(){
        $('.loader').hide();
        $.unblockUI();
    });

	$("#clients-logo").owlCarousel({
		autoPlay: 3000,
		items : 5,
		itemsDesktop : [1199,5],
		itemsDesktopSmall : [979,5],
	});

	$("#works-logo").owlCarousel({
		autoPlay: 3000,
		items : 5,
		itemsDesktop : [1199,5],
		itemsDesktopSmall : [979,5],
	});


	// google map
		var map;
		function initMap() {
		  map = new google.maps.Map(document.getElementById('map'), {
		    center: {lat: -34.397, lng: 150.644},
		    zoom: 8
		  });
		}


	// Counter

	$('.counter').counterUp({
        delay: 10,
        time: 1000
    });

	$(window).keydown(function(event){
    	if(event.keyCode == 13) {
            event.preventDefault();
      		event.target.blur();
    	}
  	});

    $(window).keydown(function(event){
        if(event.keyCode == 13) {
            $(this).blur();
        }
    });

	$(document).on("keydown", function (e) {
   	 if (e.which === 8 && !$(e.target).is("input, textarea")) {
        e.preventDefault();
    }
    });
});




