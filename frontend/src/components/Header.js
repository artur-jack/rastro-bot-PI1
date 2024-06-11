import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Header.css';
import logo from '../assets/logo.png';
import backButtonImage from '../assets/backbutton.png';

const Header = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const handleGoBack = () => {
        navigate(-1);
    };

    const showBackButton = location.pathname !== '/';

    return (
        <header className="header">
            <div className="logo-container">
                <img src={logo} alt="Logo" className="logo" />
            </div>
            <div className="title-container">
                <h1 className="title">Rastrobot</h1>
            </div>
            {showBackButton && (
                <div className="back-button-container">
                    <button onClick={handleGoBack} className="back-button">
                        <img src={backButtonImage} alt="Back" className="back-button-image" />
                    </button>
                </div>
            )}
        </header>
    );
};

export default Header;
