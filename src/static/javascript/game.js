const container = document.getElementById('container');
const stats = document.getElementById('stats');
const queue = document.getElementById('queue');

var sessionId = $(container).data('session')

function Game() {
    var grid = null;
    //update(_grid, true);
    
    function clear(element){
        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }
    }
    
    function update_grid(_grid, initial=false){
        if (initial != true){
            clear(container);
        }
        
        grid = _grid;        
        if(grid != null){
            var rows = grid.length;
            var cols = grid[0].length;
            
            for (let row = 0; row < rows; row++){
                const rowElement = document.createElement('div');
                rowElement.className = 'row';
                const rowArr = [];
                
                for (let col = 0; col < cols; col++){
                    const cell = document.createElement('div');
                    
                    if (grid[row][col] > 0){
                        cell.className = 'cell';
                        
                        const txtblock = document.createElement('div');                    
                        txtblock.textContent = grid[row][col];
                        txtblock.className = 'cell-label';
                        
                        cell.append(txtblock);
                        
                    }else if (grid[row][col] == 0) {
                        cell.className = 'cell';
                    }
                    else {
                        cell.className = 'cell-block';
                    }
                    
                    cell.setAttribute('data-row', row);
                    cell.setAttribute('data-col', col);
                    cell.addEventListener('click', function(){
                        console.log($(this)[0].textContent, col, row);
                        $.ajax({
                            type: 'POST',
                            data: {'row': row, 'col': col, 'session': sessionId},
                            url: '/api/game/update',
                            success: function(data){
                                newField = data['field'];
                                update_grid(newField);
                                update_queue(data['queue'])
                                update_stats(data['points'], data['step'], data['gameover'], data['timeout'])
                            }
                        });
                    });
                    
                    rowElement.appendChild(cell);
                    rowArr.push(cell);
                }
                
                container.appendChild(rowElement);
                grid.push(rowArr);    
            }
        }
    };
    
    
    function update_queue(queueList){
        console.log("Queue: " + queueList);
        clear(queue);
        
        $(queueList).each(function(i, v){
            console.log('Q: ' + i + ' ' + v);
            var ele = document.createElement('div');
            if(i==0){
                ele.className = 'queue-element-first';
            }else{                
                ele.className = 'queue-element';
            }
            ele.textContent = v;
            queue.appendChild(ele);
        }) 
    };
    
    function update_stats(points, step, gameover, timeout) {
        console.log("Stats: " + points + " " + step + " " + gameover) 
        clear(stats)
        var statusText = "Points: " + points;
        if(gameover){
            statusText = "--Gameover-- (" + points +")"
            
            const veil = document.createElement('div');
            veil.className = 'veil';
            
            const input_box = document.createElement('div');
            const text_box = document.createElement('div');
            text_box.textContent = 'Join the Leaderboard!';            
            text_box.className = 'textbox';
            
            const pts_box = document.createElement('div');
            pts_box.textContent = 'You reached ' + points + ' Points!'
            
            
            input_box.className = 'leaderboard-join';
            
            input_box.append(text_box);
            input_box.append(pts_box);
                        
            const input_field = document.createElement('input');
            input_field.id = 'input-username';
            $(input_field).on('keypress', function (event) {
                var regex = new RegExp("^[a-zA-Z0-9]+$");
                var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
                if (!regex.test(key)) {
                   event.preventDefault();
                   return false;
                }
            });
            
            const btn_send = document.createElement('div');
            btn_send.className = 'btn-send';
            btn_send.innerHTML = 'send';
            
            const info_box = document.createElement('div');
            info_box.className = 'infobox';
            
            btn_send.addEventListener('click', function(){
                var username = $('#input-username')[0].value;
                $('.infobox')[0].textContent = "";
                
                
                if (username.length >= 4) {
                    $.ajax({
                        type: 'POST',
                        data: {'session': sessionId, 'username': username},
                        url: '/api/leaderboard',
                        success: function(data){
                            window.open('/', '_self');
                        }
                    });
                } else {
                    $('.infobox')[0].textContent += "Username is not long enough!";
                }             
                
            });
            
            input_box.append(input_field);
            input_box.append(btn_send)
            input_box.append(info_box)
            
            $(document.body).append(veil);
            $(document.body).append(input_box);
        }
        
        if(timeout){
            statusText  = "you timed out..."
        };
        
        stats.textContent = statusText;
        
        if(timeout){
            setTimeout(function(){
                window.open('/', '_self');
            }, 3000);            
        }
    };
    
    return {
        update_grid,
        update_queue,
        update_stats,
    };
}


var game = Game()
