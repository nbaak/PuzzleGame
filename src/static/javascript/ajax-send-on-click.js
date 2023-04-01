
$('#container').ready(function(){
    $('.cell').click(function(){
        var row = $(this).data('row')
        var col = $(this).data('col')
        
        $.ajax({
    		type: 'POST',
    		data: {'row': row, 'col': col},
    		url: '/update',
    		success: function(msg){
    		}
    	});
    	
    });
})

