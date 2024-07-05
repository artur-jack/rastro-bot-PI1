import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Corridas.css';

const Corridas = () => {
  const races = [
    { id: 1, name: "Corrida 1" },
    { id: 2, name: "Corrida 2" },
    { id: 3, name: "Corrida 3" },
    { id: 4, name: "Corrida 4" }
  ];

  const navigate = useNavigate();

  const handleRaceClick = (raceId) => {
    navigate(`/corrida-anterior/${raceId}`);
  };

  return (
    <div className="corridas-container">
      <div className="corridas-button-container">
        <h2>Histórico de Corridas</h2>
        {races.map((race) => (
          <button key={race.id} className="btn" onClick={() => handleRaceClick(race.id)}>
            {race.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Corridas;
