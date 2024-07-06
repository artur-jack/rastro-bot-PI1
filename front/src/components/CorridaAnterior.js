import React from 'react';
import './CorridaAtual.css';
import FirstCorrida from './FirstCorrida';
import { useParams } from 'react-router-dom';
import MapaCorrida from './MapaCorrida';

const CorridaAnterior = () => {
  const { corridaId } = useParams();

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
              <td><FirstCorrida corridaId={corridaId} field="trajeto_total"/></td>
            </tr>
            <tr>
              <td>Tempo de Percurso</td>
              <td><FirstCorrida corridaId={corridaId} field="tempo_total" /></td>
            </tr>
            <tr>
              <td>Velocidade Instantânea</td>
              <td><FirstCorrida corridaId={corridaId} field="velocidade_media"/></td>
            </tr>
            <tr>
              <td>Aceleração Instantânea</td>
              <td><FirstCorrida corridaId={corridaId} field="aceleracao_media"/></td>
            </tr>
            <tr>
              <td>Consumo Energético</td>
              <td><FirstCorrida corridaId={corridaId} field = "consumo_medio"/></td>
            </tr>
          </tbody>
        </table>
      </div>
      <MapaCorrida corridaId={corridaId} />
    </div>
  );
};

export default CorridaAnterior;
