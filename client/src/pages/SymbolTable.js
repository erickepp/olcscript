import { useEffect } from 'react';

function SymbolTable() {
  const symbolTableJSON = localStorage.getItem('symbolTable');
  const symbolTable = symbolTableJSON ? JSON.parse(symbolTableJSON) : [];
  const rows = symbolTable.map((symbol, index) => (
    <tr key={index}>
      <td>{symbol.id}</td>
      <td>{symbol.symbolType}</td>
      <td>{symbol.dataType}</td>
      <td>{symbol.scope}</td>
      <td>{symbol.line}</td>
    </tr>
  ));

  useEffect(() => {
    document.title = 'OLCScript - Tabla de símbolos';
  });

  return (
    <div class="container">
      <h1 style={{ color: 'white', textAlign: 'center', margin: '2%' }}>Tabla de símbolos</h1>

      <table class="table table-dark table-hover">
        <thead style={{ borderBottom: '1px solid white' }}>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Tipo símbolo</th>
            <th scope="col">Tipo dato</th>
            <th scope="col">Ámbito</th>
            <th scope="col">Línea</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  );
}

export default SymbolTable;
