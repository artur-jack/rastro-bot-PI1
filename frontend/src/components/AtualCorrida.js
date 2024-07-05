import React, { useEffect, useState } from 'react';
import axios from 'axios';

const CorridaAtual = () => {
  const [metrics, setCorrida] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCorrida = async () => {
      try {
        const response = await axios.get('http://localhost:3000/api/real_time');
        setCorrida(response.data); 
      } catch (err) {
        setError(err.message); 
      }
    };

    fetchCorrida();
  }, []); 

  if (error) return <div>Erro: {error}</div>; 

  return (
    <div>
      {metrics ? (
        <div>
          <h2>Corrida Atual</h2>
          <p>Trajeto Percorrido: {metrics.data.total_distance}</p>
          <p>Tempo de Percurso: {metrics.data.timestamp}</p>
          <p>Velocidade Instantânea: {metrics.data.speed}</p>
          <p>Aceleração Instantânea: {metrics.data.acceleration}</p>
          <p>Consumo Energético: {metrics.data.consumption}</p>
        </div>
      ) : (
        <p>Nenhuma metrics encontrada.</p>
      )}
    </div>
  );
};

export default CorridaAtual;

