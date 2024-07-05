import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './CorridaAtual.css';

const CorridaAtual = () => {
  const [metrics, setCorrida] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCorrida = async () => {
      try {
        const response = await axios.get('http://localhost:3000/api/real_time');
        setCorrida(response.data); 
        setError(null); 
      } catch (err) {
        setError(err.message); 
      }
    };

    fetchCorrida(); 

    const interval = setInterval(fetchCorrida, 5000); 

    return () => clearInterval(interval); 
  }, []); 

  if (error) return <div>Erro: {error}</div>; 

  return (
    <div className='corrida-container'>
      <h2>Corrida Atual</h2>
      <div className='table-container'>
        <table>
          <tbody>
            <tr>
              <td>Medida</td>
              <td>Valor</td>
            </tr>
            <tr>
              <td>Trajeto Percorrido</td>
              <td>{metrics ? metrics.data.total_distance : '---'}</td>
            </tr>
            <tr>
              <td>Tempo de Percurso</td>
              <td>{metrics ? metrics.data.timestamp : '---'}</td>
            </tr>
            <tr>
              <td>Velocidade Instantânea</td>
              <td>{metrics ? metrics.data.speed : '---'}</td>
            </tr>
            <tr>
              <td>Aceleração Instantânea</td>
              <td>{metrics ? metrics.data.acceleration : '---'}</td>
            </tr>
            <tr>
              <td>Consumo Energético</td>
              <td>{metrics ? metrics.data.consumption : '---'}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CorridaAtual;
