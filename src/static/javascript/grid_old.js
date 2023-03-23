/** OLD */
function createGridOLD(n, m) {
  const grid = [];
  
  for (let i = 0; i < n; i++) {
    const row = document.createElement('div');
    row.className = 'row';
    const rowArr = [];
    for (let j = 0; j < m; j++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.textContent = i*j;
      cell.setAttribute('data-row', i);
      cell.setAttribute('data-col', j);
      row.appendChild(cell);
      rowArr.push(cell);
    }
    container.appendChild(row);
    grid.push(rowArr);
  }
  
  function setCellValue(row, col, value) {
    if (row < 0 || row >= n || col < 0 || col >= m) {
      console.error('Invalid row or column');
      return;
    }
    grid[row][col].textContent = value;
  }
  
  function setCellColor(row, col, color) {
    if (row < 0 || row >= n || col < 0 || col >= m) {
      console.error('Invalid row or column');
      return;
    }
    grid[row][col].style.backgroundColor = color;
  }
  
  return {
    setCellValue,
    setCellColor,
  };
}

//const myGrid = createGrid(3, 4);

/*
const myGrid = createGrid(3, 4); // Creates a grid of 5 rows and 7 cells per row
myGrid.setCellValue(0, 0, '.');
myGrid.setCellColor(0, 0, 'red');

myGrid.setCellValue(0, 1, '.');
myGrid.setCellColor(0, 1, 'blue');

myGrid.setCellValue(0, 2, '.');
myGrid.setCellColor(0, 2, 'green');

myGrid.setCellValue(0, 3, '.');
myGrid.setCellColor(0, 3, 'red');
*/