import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Content.css';

const Content = () => {
    const [showCorridas, setShowCorridas] = useState(false);

  const [percursoIniciado, setPercursoIniciado] = useState(false);
  const navigate = useNavigate();

  const handleShowCorridas = () => {
    setShowCorridas(true);
    navigate('/corridas'); // Redireciona para a página de histórico de corridas
  };

  const handleStartPercurso = () => {
    setPercursoIniciado(true);
    alert('Percurso iniciado com sucesso!');
    navigate('/corrida-atual'); 

  };

  return (
    <div className="content">
      <div className="button-container">
      <h2>Bem-vindo!</h2>
        <button className="btn" onClick={handleStartPercurso}>
          {percursoIniciado ? 'Acompanhar Percurso' : 'Iniciar Percurso'}
        </button>
        <button className="btn" onClick={handleShowCorridas}>Ver Histórico de Corridas</button>
      </div>
    </div>
  );
};

export default Content;

