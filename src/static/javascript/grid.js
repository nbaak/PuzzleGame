const container = document.getElementById('container');

var sessionId = $(container).data('session')

function Game() {
    var grid = null;
    //update(_grid, true);
    
    function clear(){
        while (container.firstChild) {
            container.removeChild(container.firstChild);
        }
    }
    
    function update_grid(_grid, initial=false){
        if (initial != true){
            clear();
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
    
    
    function update_queue(queue){
        console.log("Queue: " + queue);
    }
    
    function update_stats(points, step) {
        console.log("Stats: " + points + " " + step)
    }
    
    return {
        update: update_grid,
        clear,
    }
}


var game = Game()
