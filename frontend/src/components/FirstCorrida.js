import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const FirstCorrida = ({ corridaId, field }) => {
  const [corrida, setCorrida] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCorrida = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`http://localhost:3000/api/corrida/${corridaId}`);
        if (response.data.data) {
          setCorrida(response.data.data);
        } else {
          setCorrida(null);
        }
        setLoading(false);
      } catch (err) {
        setError(err.message); // Captura apenas a mensagem de erro
        setLoading(false);
      }
    };

    fetchCorrida();
  }, [corridaId]); // Reexecuta o efeito sempre que corridaId mudar

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>; // Exibe o erro capturado

  return (
    <div>
      {corrida ? (
        <p>{corrida[field]}</p>
      ) : (
        <p>Nenhuma corrida encontrada com o ID {corridaId}.</p>
      )}
    </div>
  );
};

export default FirstCorrida;
