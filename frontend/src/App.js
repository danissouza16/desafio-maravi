import React, { useState } from 'react';
import './App.css';
import AlertaForm from './components/AlertaForm';
import Dashboard from './components/Dashboard'; 

function App() {
  const [pagina, setPagina] = useState('alerta'); // Controla qual página exibir

  return (
    <div className="App">
      <header className="App-header">
        <h1>Maravi Bus</h1>
        <nav>
          <button onClick={() => setPagina('alerta')} style={{marginRight: '10px'}}>Criar Alerta</button>
          <button onClick={() => setPagina('dashboard')}>Ver Mapa (Dashboard)</button>
        </nav>
      </header>
      
      <main>
        {pagina === 'alerta' ? <AlertaForm /> : <Dashboard />}
      </main>
    </div>
  );
}

export default App;
