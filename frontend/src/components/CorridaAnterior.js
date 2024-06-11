import React from 'react';
import './CorridaAtual.css';

const CorridaAnterior = () => {
  return (
    <div className='corrida-container'>
      <h2>Corrida Anterior</h2>
      <div className='table-container'> 
        <table>
          <tbody>
            <tr>
              <td>Medida</td>
              <td>Valor</td>
            </tr>
            <tr>
              <td>Trajeto Percorrido</td>
              <td></td>
            </tr>
            <tr>
              <td>Tempo de Percurso</td>
              <td></td>
            </tr>
            <tr>
              <td>Velocidade Instantânea</td>
              <td></td>
            </tr>
            <tr>
              <td>Aceleração Instantânea</td>
              <td></td>
            </tr>
            <tr>
              <td>Consumo Energético</td>
              <td></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CorridaAnterior;
