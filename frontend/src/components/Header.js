import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import './Header.css'; 
import logo from '../assets/logo.png';
import backButtonImage from '../assets/backbutton.png'; 

const Header = () => {
  const navigate = useNavigate(); 

  const handleGoBack = () => {
    navigate(-1); 
  };

  return (
    <header className="header">
      <div className="logo-container">
        <img src={logo} alt="Logo" className="logo" />
      </div>
      <div className="title-container">
        <h1 className="title">Rastrobot</h1>
      </div>
      <div className="back-button-container">
        <button onClick={handleGoBack} className="back-button">
          <img src={backButtonImage} alt="Back" className="back-button-image" />
        </button>
      </div>
    </header>
  );
};

export default Header;
