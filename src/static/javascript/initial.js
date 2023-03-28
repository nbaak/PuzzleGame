
function setField(data){
    game.update_grid(data['field']);
    game.update_queue(data['queue']);
    game.update_stats(data['points'], data['step'], data['gameover']);
} 

$('#container').ready(function(){

    $.ajax({
        type: 'POST',
        data: {'session': sessionId},
        url: '/api/game/initial',
        success: function(data){
            console.log(data);
            
            setField(data);
        }
    });
    
})