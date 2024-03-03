import { useEffect } from 'react';

function Errors() {
  const errorsJSON = localStorage.getItem('errors');
  const errors = errorsJSON ? JSON.parse(errorsJSON) : [];
  const rows = errors.map((error, index) => (
    <tr key={index}>
      <th scope="row">{index + 1}</th>
      <td>{error.description}</td>
      <td>{error.line}</td>
      <td>{error.col}</td>
      <td>{error.type}</td>
    </tr>
  ));

  useEffect(() => {
    document.title = 'OLCScript - Errores';
  });

  return (
    <div class="container">
      <h1 style={{ color: 'white', textAlign: 'center', margin: '2%' }}>Errores</h1>

      <table class="table table-dark table-hover">
        <thead style={{ borderBottom: '1px solid white' }}>
          <tr>
            <th scope="col">No.</th>
            <th scope="col">Descripción</th>
            <th scope="col">Línea</th>
            <th scope="col">Columna</th>
            <th scope="col">Tipo</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  );
}

export default Errors;
