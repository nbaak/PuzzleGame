
function setField(field){
    myGrid.update(field);
} 

$('#container').ready(function(){
    
    $.getJSON('/update', function(data){
        field = data['field'];
        queue = data['queue'];
        
        setField(field);
    })
    
    /* if /update is only POST
    $.ajax({
        type: 'POST',
        data: {},
        url: '/update',
        success: function(data){
            console.log(data);
            
            setField(data['field']);
        }
    });
    */
})