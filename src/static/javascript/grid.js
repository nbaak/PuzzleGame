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
                        url: '/update',
                        success: function(data){
                            newField = data['field'];
                            update_grid(newField);
                            update_queue(data['queue'])
                            update_stats(data['points'], data['step'])
                        }
                    });
                });
                
                rowElement.appendChild(cell);
                rowArr.push(cell);
            }
            
            container.appendChild(rowElement);
            grid.push(rowArr);    
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
    }
    
    function update_stats(points, step) {
        console.log("Stats: " + points + " " + step)
        clear(stats)
        stats.textContent = "Points: " + points ; //TODO: + " Step: " + step
    }
    
    return {
        update: update_grid,
        clear,
    }
}


var game = Game()
