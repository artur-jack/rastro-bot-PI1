import React from 'react';
import { Route, BrowserRouter, Routes } from "react-router-dom";
import Header from './components/Header';
import Content from './components/Content';
import Corridas from './components/Corridas';
import CorridaAtual from './components/CorridaAtual';
import CorridaAnterior from './components/CorridaAnterior';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" exact element={<Content/>} />
          <Route path="/corridas" element={<Corridas/>} />
          <Route path="/corrida-atual" element={<CorridaAtual />} />
          <Route path="/corrida-anterior" element={<CorridaAnterior />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;