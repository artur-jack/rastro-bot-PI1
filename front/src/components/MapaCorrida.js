import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const MapaCorrida = ({ corridaId }) => {
  const [data, setData] = useState({
    labels: [],
    datasets: [{
      label: 'Posições do Carrinho',
      data: [],
      borderColor: 'rgba(75,192,192,1)',
      fill: false,
    }]
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:3000/api/corrida/${corridaId}/readings`);
        const result = await response.json();
        if (result.data && result.data.posicoes) {
          const posicoes = result.data.posicoes;
          setData({
            labels: posicoes.map((_, index) => index), // Use o índice como label
            datasets: [{
              label: 'Posições do Carrinho',
              data: posicoes.map(posicao => ({ x: posicao.x, y: posicao.y })),
              borderColor: 'rgba(75,192,192,1)',
              fill: false,
              tension: 0.1
            }]
          });
        }
      } catch (error) {
        console.error('Erro ao buscar dados:', error);
      }
    };

    fetchData();
  }, [corridaId]);

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column' }}>
      <h2>Mapa da Corrida</h2>
      <div style={{ width: '100%', maxWidth: '800px' }}>
        <Line 
          data={data} 
          options={{
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: { type: 'linear', position: 'bottom' },
              y: { beginAtZero: true }
            }
          }} 
          height={400} // Altura fixa para garantir que o gráfico tenha um tamanho adequado
        />
      </div>
    </div>
  );
};

export default MapaCorrida;
