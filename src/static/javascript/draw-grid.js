
function setField(field){
    game.update(field);
} 

$('#container').ready(function(){

    $.ajax({
        type: 'POST',
        data: {'session': sessionId},
        url: '/initial',
        success: function(data){
            console.log(data);
            
            setField(data['field']);
        }
    });
    
})