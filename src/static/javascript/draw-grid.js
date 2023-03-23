
function setField(field){
    myGrid.update(field);
} 

$('#container').ready(function(){
    
    /*
    $.getJSON('/update', function(data){
        field = data['field'];
        queue = data['queue'];
        
        setField(field);
    })
    */
    
    // update is only POST
    $.ajax({
        type: 'POST',
        data: {'row': -1, 'col': -1, 'session': sessionId},
        url: '/update',
        success: function(data){
            console.log(data);
            
            setField(data['field']);
        }
    });
    
})