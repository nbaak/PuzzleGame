const container = document.getElementById('container');

var sessionId = $(container).data('session')

function createGrid(_grid) {
	var grid = _grid;
	update(_grid, true);
    
    function clear(){
		while (container.firstChild) {
            container.removeChild(container.firstChild);
        }
	}
    
    function update(_grid, initial=false){
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
                cell.className = 'cell';
                cell.textContent = grid[row][col];
                
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
							update(newField);
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
	
	return {
		update,
		clear,
	}
}


myGrid = createGrid([[1,2], [3,4]])



