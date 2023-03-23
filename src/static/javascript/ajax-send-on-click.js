
$('#container').ready(function(){
	console.log("READY");
    $('.cell').click(function(){
        var row = $(this).data('row')
        var col = $(this).data('col')
        console.log($(this)[0].textContent, col, row);
        
        $.ajax({
    		type: 'POST',
    		data: {'row': row, 'col': col},
    		url: '/update',
    		success: function(msg){
    			console.log('recv: ' + msg)
    		}
    	});
    	
    });
})

