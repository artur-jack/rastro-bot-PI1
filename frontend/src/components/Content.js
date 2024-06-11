import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Content.css';

const Content = () => {
  const [showCorridas, setShowCorridas] = useState(false);
  const [percursoIniciado, setPercursoIniciado] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const percursoIniciadoSesionStorage = sessionStorage.getItem('percursoIniciado');
    if (percursoIniciadoSesionStorage === 'true') {
      setPercursoIniciado(true);
    } else {
      setPercursoIniciado(false);
    }
  }, []);

  const handleShowCorridas = () => {
    setShowCorridas(true);
    navigate('/corridas'); // Redireciona para a página de histórico de corridas
  };

  const handleStartPercurso = () => {
    setPercursoIniciado(true);
    sessionStorage.setItem('percursoIniciado', 'true'); // Salva o estado no Local Storage
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
