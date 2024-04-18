import React from 'react';

function Tabla(props) {
  const { resultados, titulo = "Resultados individuales"} = props;

  // Función para crear una fila de la tabla de resultados
  function crearFila(res, index) {
    return (
      <tr key={index}>
        <td>{index}</td>
        <td>{res.review_es}</td>
        <td>{res.sentimiento}</td>
      </tr>
    );
  }

  return (
    <div>
      <br></br>
      <h2>{titulo}</h2>
      <br></br>
      <table className="table table-hover table-striped">
        <thead>
          <tr>
          <th  scope="col">#</th>
            <th  scope="col">Reseña</th>
            <th  scope="col">Sentimiento</th>
          </tr>
        </thead>
        <tbody>
          {console.log(resultados)}
           { resultados.map((res, index) => crearFila(res, index))}
        </tbody>
      </table>

    </div>
  );
}

export default Tabla;