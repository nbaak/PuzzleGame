

$(document).ready(function(){

    $('.button').click(function(){
        window.open($(this).data('src'), '_self');
    });

});