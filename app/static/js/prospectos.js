$(document).ready(function() {
    $('input[name="prospecto"]').click(function() {
        $('tr.selected').removeClass('selected');
        $('#prospecto-' + $(this).attr('id')).addClass('selected');
        $('#prospecto').val($(this).attr('id'));
    });

    $('input[type="submit"]').click(function() {
        $('.loader').show();
    });
});