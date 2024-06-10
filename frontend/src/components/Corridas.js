import React from 'react';
import './Corridas.css';

const Corridas = () => {
  const raceNames = ["Corrida 1", "Corrida 2", "Corrida 3", "Corrida 4"];

  return (
    <div className="corridas-container">
      <div className="corridas-button-container">
        <h2>Histórico de Corridas</h2>
        {raceNames.map((raceName, index) => (
          <button key={index} className="btn">{raceName}</button>
        ))}
      </div>
    </div>
  );
};

export default Corridas;
